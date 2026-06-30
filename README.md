# Boredom Study — Web App

A three-arm between-subjects psychology experiment with server-side permuted-block
randomization, per-page partial saving, an admin panel, and `.xlsx` export.

## Quick start (local)

```bash
cd boredom_study
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py          # starts on http://localhost:5000
```

Open `http://localhost:5000` to run through the study as a participant.
Open `http://localhost:5000/admin` (password: `changeme`) for the admin panel.

To test without a Prolific ID (TEST_MODE): just visit `http://localhost:5000` directly.
To simulate a Prolific participant: `http://localhost:5000?PROLIFIC_PID=test123&STUDY_ID=s1&SESSION_ID=sess1`

## Configuration (environment variables)

| Variable | Default | Description |
|----------|---------|-------------|
| SECRET_KEY | (insecure default) | Flask session signing key — **change before deploying** |
| DATABASE_PATH | `study.db` | Path to SQLite file |
| ADMIN_PASSWORD | `changeme` | Admin panel password — **change before deploying** |
| PROLIFIC_COMPLETION_URL | placeholder | Prolific redirect URL with completion code |
| MIN_WRITING_TIME_SEC | `180` | Minimum time on writing page (seconds) |
| MIN_WRITING_CHARS | `400` | Minimum character count for essay |
| BORING_TASK_DURATION_SEC | `300` | Duration of the CPT attention task |
| BORING_TASK_TARGET | `X` | Target letter for the CPT |
| RNG_SEED | (none) | Integer seed for reproducible test runs |
| FORCE_DESKTOP | `true` | Show desktop recommendation warning on mobile |

Set these in a `.env` file (with `python-dotenv`) or as shell exports before running.

## Deploying to Railway (free tier)

1. Push this folder to a GitHub repository.
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub.
3. Railway detects Python; set the start command to:
   ```
   gunicorn app:app
   ```
4. Add environment variables in the Railway dashboard (SECRET_KEY, ADMIN_PASSWORD,
   PROLIFIC_COMPLETION_URL, DATABASE_PATH=/data/study.db).
5. Add a persistent volume mounted at `/data` so the SQLite file survives deploys.
6. Your study URL will be something like `https://your-app.up.railway.app`.

## Deploying to Render (free tier)

1. Push to GitHub.
2. Render → New Web Service → connect repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Add env vars (same as above). Use a Render Disk for persistent storage.

## Content you must add before running with real participants

All items marked `[PLACEHOLDER]` in the source must be replaced:

- `templates/consent.html` — IRB consent text
- `templates/debrief.html` — debrief text
- `app.py` (WRITING_PROMPTS dict) — final wording of the three writing prompts
- `app.py` (BPS_ITEMS, MLQ_ITEMS, AUTOTRAIT_ITEMS, STATEMEAN_ITEMS, STATEAUTO_ITEMS, MSBS_ITEMS) — exact verbatim items from published instruments
- `Config.PROLIFIC_COMPLETION_URL` — your actual Prolific completion URL

## Randomization

Participants are assigned using **permuted-block randomization** with block sizes
randomly drawn from {3, 6, 9}. Within each block, all three conditions appear equally
often in random order. This guarantees that at every multiple of 3 participants, the
three arms are exactly balanced. Assignment is server-side and idempotent (refresh-safe).

## Data

- `study.db` — SQLite database (source of truth)
- Admin → Download data (.xlsx) — master workbook + counts sheet
- Admin → Download SQLite backup — raw database file

See `codebook.md` for the full data dictionary.
