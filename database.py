import os
import sqlite3
import json
from config import Config


def get_db(path=None):
    target = path or Config.DATABASE_PATH
    os.makedirs(os.path.dirname(target) or '.', exist_ok=True)
    db = sqlite3.connect(target)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA journal_mode=WAL')
    return db


def init_db(path=None):
    db = get_db(path)
    db.executescript('''
        CREATE TABLE IF NOT EXISTS participants (
            participant_id      TEXT PRIMARY KEY,
            prolific_pid        TEXT,
            study_id            TEXT,
            session_id          TEXT,
            test_mode           INTEGER DEFAULT 0,
            condition           TEXT,
            assignment_timestamp TEXT,
            current_step        TEXT DEFAULT 'entry',
            start_timestamp     TEXT,
            finish_timestamp    TEXT,
            total_duration_sec  REAL,
            completed           INTEGER DEFAULT 0,
            consent             INTEGER DEFAULT 0,
            consent_timestamp   TEXT,
            attention_check_pass INTEGER,
            user_agent          TEXT,
            screen_w            INTEGER,
            screen_h            INTEGER,

            -- Trait scales (placeholders; extend item count to match actual instruments)
            bps_1 INTEGER, bps_2 INTEGER, bps_3 INTEGER, bps_4 INTEGER,
            bps_5 INTEGER, bps_6 INTEGER, bps_7 INTEGER, bps_8 INTEGER,
            bps_order TEXT,

            mlq_1 INTEGER, mlq_2 INTEGER, mlq_3 INTEGER, mlq_4 INTEGER, mlq_5 INTEGER,
            mlq_6 INTEGER, mlq_7 INTEGER, mlq_8 INTEGER, mlq_9 INTEGER, mlq_10 INTEGER,
            mlq_order TEXT,

            -- old autotrait columns kept for migration compatibility (no longer collected)
            autotrait_1 INTEGER, autotrait_2 INTEGER, autotrait_3 INTEGER,
            autotrait_4 INTEGER, autotrait_5 INTEGER, autotrait_6 INTEGER,
            autotrait_order TEXT,

            -- Subjective Personal Agency (Yamaguchi et al., 2025) — 1–5
            spa_1 INTEGER, spa_2 INTEGER, spa_3 INTEGER, spa_4 INTEGER, spa_5 INTEGER,
            spa_order TEXT,

            -- BPNS Autonomy Subscale (Deci & Ryan, 2000; Johnston & Finney, 2010) — 1–7
            bpns_1 INTEGER, bpns_2 INTEGER, bpns_3 INTEGER, bpns_4 INTEGER,
            bpns_5 INTEGER, bpns_6 INTEGER, bpns_7 INTEGER,
            bpns_order TEXT,

            -- BPNSF Autonomy Sat. & Frust. (Chen et al., 2015) — 1–5
            bpnsf_1 INTEGER, bpnsf_2 INTEGER, bpnsf_3 INTEGER, bpnsf_4 INTEGER,
            bpnsf_5 INTEGER, bpnsf_6 INTEGER, bpnsf_7 INTEGER, bpnsf_8 INTEGER,
            bpnsf_order TEXT,

            -- General Self-Efficacy (Schwarzer & Jerusalem, 1995) — 1–4
            se_1 INTEGER, se_2 INTEGER, se_3 INTEGER, se_4 INTEGER, se_5 INTEGER,
            se_6 INTEGER, se_7 INTEGER, se_8 INTEGER, se_9 INTEGER, se_10 INTEGER,
            se_order TEXT,

            scale_block_order TEXT,

            -- Demographics
            demo_age              INTEGER,
            demo_gender           TEXT,
            demo_relationship     TEXT,
            demo_ethnicity        TEXT,
            demo_race             TEXT,
            demo_race_other       TEXT,

            -- Objective SES
            ses_education         INTEGER,
            ses_household_income  INTEGER,
            ses_personal_income   INTEGER,
            ses_employment        TEXT,
            ses_job_title         TEXT,

            -- Subjective SES ladders (Adler et al., 2000) — 10=best/most, 1=worst/least
            ladder_education      INTEGER,
            ladder_money          INTEGER,
            ladder_job            INTEGER,

            -- Sociometric status ladders (Mahadevan et al., 2021) — 10=most, 1=least
            sociometric_respect   INTEGER,
            sociometric_admired   INTEGER,
            sociometric_important INTEGER,

            -- Writing manipulation
            writing_text        TEXT,
            writing_time_sec    REAL,
            writing_charcount   INTEGER,

            -- Manipulation check
            statemean_1 INTEGER, statemean_2 INTEGER, statemean_3 INTEGER, statemean_4 INTEGER,
            statemean_5 INTEGER,
            stateauto_1 INTEGER, stateauto_2 INTEGER, stateauto_3 INTEGER, stateauto_4 INTEGER,
            stateauto_5 INTEGER, stateauto_6 INTEGER, stateauto_7 INTEGER, stateauto_8 INTEGER,
            mancheck_order TEXT,

            -- Boring task (transcription)
            boringtask_duration_sec  REAL,
            transcription_text       TEXT,
            transcription_accuracy   REAL,
            transcription_charcount  INTEGER,

            -- Outcome (MSBS short form)
            msbs_1 INTEGER, msbs_2 INTEGER, msbs_3 INTEGER, msbs_4 INTEGER,
            msbs_5 INTEGER, msbs_6 INTEGER, msbs_7 INTEGER, msbs_8 INTEGER,

            -- Page timestamps
            ts_consent       TEXT,
            ts_traits        TEXT,
            ts_demographics  TEXT,
            ts_ladders       TEXT,
            ts_writing       TEXT,
            ts_mancheck      TEXT,
            ts_boring_task   TEXT,
            ts_outcome       TEXT,
            ts_debrief       TEXT
        );

        CREATE TABLE IF NOT EXISTS randomization_state (
            id                INTEGER PRIMARY KEY,
            current_block     TEXT NOT NULL,
            condition_counts  TEXT NOT NULL,
            rng_state         TEXT NOT NULL
        );
    ''')
    db.commit()

    # Migrate existing databases: add new columns if they don't exist yet
    new_columns = [
        ('statemean_5', 'INTEGER'),
        ('stateauto_5', 'INTEGER'), ('stateauto_6', 'INTEGER'),
        ('stateauto_7', 'INTEGER'), ('stateauto_8', 'INTEGER'),
        ('spa_1','INTEGER'),('spa_2','INTEGER'),('spa_3','INTEGER'),
        ('spa_4','INTEGER'),('spa_5','INTEGER'),('spa_order','TEXT'),
        ('bpns_1','INTEGER'),('bpns_2','INTEGER'),('bpns_3','INTEGER'),
        ('bpns_4','INTEGER'),('bpns_5','INTEGER'),('bpns_6','INTEGER'),
        ('bpns_7','INTEGER'),('bpns_order','TEXT'),
        ('bpnsf_1','INTEGER'),('bpnsf_2','INTEGER'),('bpnsf_3','INTEGER'),
        ('bpnsf_4','INTEGER'),('bpnsf_5','INTEGER'),('bpnsf_6','INTEGER'),
        ('bpnsf_7','INTEGER'),('bpnsf_8','INTEGER'),('bpnsf_order','TEXT'),
        ('se_1','INTEGER'),('se_2','INTEGER'),('se_3','INTEGER'),('se_4','INTEGER'),
        ('se_5','INTEGER'),('se_6','INTEGER'),('se_7','INTEGER'),('se_8','INTEGER'),
        ('se_9','INTEGER'),('se_10','INTEGER'),('se_order','TEXT'),
        ('transcription_text',      'TEXT'),
        ('transcription_accuracy',  'REAL'),
        ('transcription_charcount', 'INTEGER'),
        ('demo_relationship',       'TEXT'),
        ('demo_ethnicity',          'TEXT'),
        ('demo_race',               'TEXT'),
        ('demo_race_other',         'TEXT'),
        ('ses_household_income',    'INTEGER'),
        ('ses_personal_income',     'INTEGER'),
        ('ses_employment',          'TEXT'),
        ('ses_job_title',           'TEXT'),
        ('ladder_education',        'INTEGER'),
        ('ladder_money',            'INTEGER'),
        ('ladder_job',              'INTEGER'),
        ('sociometric_respect',     'INTEGER'),
        ('sociometric_admired',     'INTEGER'),
        ('sociometric_important',   'INTEGER'),
        ('ts_ladders',              'TEXT'),
    ]
    for col, col_type in new_columns:
        try:
            db.execute(f'ALTER TABLE participants ADD COLUMN {col} {col_type}')
            db.commit()
        except Exception:
            pass  # column already exists

    db.close()


def get_participant(db, participant_id):
    return db.execute(
        'SELECT * FROM participants WHERE participant_id = ?', (participant_id,)
    ).fetchone()


def create_participant(db, data: dict):
    cols = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    db.execute(
        f'INSERT OR IGNORE INTO participants ({cols}) VALUES ({placeholders})',
        list(data.values())
    )
    db.commit()


def update_participant(db, participant_id, data: dict):
    if not data:
        return
    set_clause = ', '.join(f'{k} = ?' for k in data.keys())
    db.execute(
        f'UPDATE participants SET {set_clause} WHERE participant_id = ?',
        list(data.values()) + [participant_id]
    )
    db.commit()


def get_all_participants(db):
    return db.execute('SELECT * FROM participants ORDER BY start_timestamp').fetchall()


def get_condition_counts(db):
    rows = db.execute(
        "SELECT condition, COUNT(*) as n, SUM(completed) as completed "
        "FROM participants WHERE test_mode = 0 AND condition IS NOT NULL "
        "GROUP BY condition"
    ).fetchall()
    return {r['condition']: {'n': r['n'], 'completed': r['completed'] or 0} for r in rows}


def get_summary_stats(db):
    row = db.execute(
        "SELECT COUNT(*) as total, SUM(completed) as completed, "
        "AVG(CASE WHEN completed=1 THEN total_duration_sec END) as avg_duration "
        "FROM participants WHERE test_mode = 0"
    ).fetchone()
    return dict(row)


def delete_all_data(db):
    db.execute('DELETE FROM participants')
    db.execute('DELETE FROM randomization_state')
    db.commit()
