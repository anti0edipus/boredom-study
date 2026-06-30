# Codebook — Boredom Study

One row per participant. All timestamps in UTC ISO-8601.

## IDs & Meta

| Column | Type | Values | Notes |
|--------|------|--------|-------|
| participant_id | TEXT | UUID4 | Internal primary key |
| prolific_pid | TEXT | Prolific participant ID | Empty if TEST_MODE |
| study_id | TEXT | Prolific study ID | |
| session_id | TEXT | Prolific session ID | |
| test_mode | INTEGER | 0 = real, 1 = test | Set when PROLIFIC_PID absent from URL |
| condition | TEXT | meaning / autonomy / control | Assigned by permuted-block randomizer |
| assignment_timestamp | TEXT | ISO-8601 | When condition was assigned (after demographics) |
| current_step | TEXT | consent / traits / … / completed | Last completed step; used for dropout recovery |
| start_timestamp | TEXT | ISO-8601 | Entry page load |
| finish_timestamp | TEXT | ISO-8601 | Debrief submission |
| total_duration_sec | REAL | seconds | finish − start |
| completed | INTEGER | 0 / 1 | 1 = reached debrief and submitted |
| consent | INTEGER | 0 / 1 | 1 = clicked consent checkbox |
| consent_timestamp | TEXT | ISO-8601 | |
| attention_check_pass | INTEGER | 0 / 1 | 1 = passed instructed-response item in traits |
| user_agent | TEXT | browser string | |
| screen_w / screen_h | INTEGER | pixels | Recorded at consent page |

## Trait Scales

### BPS — Boredom Proneness Scale (short form)
**PLACEHOLDER** — insert final item count, citation, and subscales.
Response scale: 1 (Strongly disagree) – 7 (Strongly agree).

| Column | Type | Notes |
|--------|------|-------|
| bps_1 … bps_8 | INTEGER | 1–7 |
| bps_order | TEXT | Comma-separated item display order |
| bps_attn | INTEGER | Attention check item (correct = 4); NOT a BPS item |

### MLQ — Meaning in Life Questionnaire
**PLACEHOLDER** — 10 items; Presence subscale (items 1,4,5,6,9R) + Search subscale (items 2,3,7,8,10). Cite Steger et al. (2006).
Response scale: 1 (Absolutely untrue) – 7 (Absolutely true). Item 9 is reverse-scored.

| Column | Type | Notes |
|--------|------|-------|
| mlq_1 … mlq_10 | INTEGER | 1–7; item 9 reverse-scored before summing |
| mlq_order | TEXT | Comma-separated item display order |

### Autonomy Trait Measure
**PLACEHOLDER** — insert instrument name and citation.
Response scale: 1 (Not at all true) – 7 (Very true).

| Column | Type | Notes |
|--------|------|-------|
| autotrait_1 … autotrait_6 | INTEGER | 1–7 |
| autotrait_order | TEXT | Comma-separated item display order |

| scale_block_order | TEXT | Comma-separated order in which the three scale blocks were shown |

## SES & Demographics

| Column | Type | Values | Notes |
|--------|------|--------|-------|
| ses_education | INTEGER | 1–6, 99 = prefer not | 1=less than HS … 6=doctoral |
| ses_income | INTEGER | 1–7, 99 = prefer not | income bands; see demographics.html |
| ses_occupation | TEXT | free text | |
| ladder | INTEGER | 1–10 | MacArthur Subjective SES Ladder |
| demo_age | INTEGER | years | |
| demo_gender | TEXT | categorical + free-text | |
| demo_country | TEXT | free text | |

## Writing Manipulation

| Column | Type | Notes |
|--------|------|-------|
| writing_text | TEXT | Full essay text |
| writing_time_sec | REAL | Time spent on writing page (seconds) |
| writing_charcount | INTEGER | Character count of essay |

## Manipulation Check

State measures collected immediately after writing, before boring task.
Response scale: 1 (Not at all) – 7 (Extremely).
**PLACEHOLDER** — insert final item text and citations.

| Column | Type | Notes |
|--------|------|-------|
| statemean_1 … statemean_4 | INTEGER | 1–7; state meaning items |
| stateauto_1 … stateauto_4 | INTEGER | 1–7; state autonomy items |
| mancheck_order | TEXT | JSON: {"mean": [...], "auto": [...]} display orders |

## Boring Task (CPT)

5-minute letter stream; press SPACEBAR for target letter (default: X).

| Column | Type | Notes |
|--------|------|-------|
| boringtask_duration_sec | REAL | Actual duration (should ≈ 300) |
| boringtask_hits | INTEGER | Correct presses within 1000ms of target |
| boringtask_misses | INTEGER | Targets with no response within 1000ms |
| boringtask_false_alarms | INTEGER | Presses on non-target letters |
| boringtask_rt_mean | REAL | Mean RT for hits (ms) |

## Outcome — MSBS (Primary DV)

Multidimensional State Boredom Scale (short form). **PLACEHOLDER** — insert citation.
Response scale: 1 (Not at all) – 7 (Extremely).

| Column | Type | Notes |
|--------|------|-------|
| msbs_1 … msbs_8 | INTEGER | 1–7 |

## Page Timestamps

| Column | Notes |
|--------|-------|
| ts_consent | When consent form was submitted |
| ts_traits | When trait scales were submitted |
| ts_demographics | When demographics were submitted |
| ts_writing | When writing task was submitted |
| ts_mancheck | When manipulation check was submitted |
| ts_boring_task | When boring task ended |
| ts_outcome | When MSBS was submitted |
| ts_debrief | When debrief was submitted (= finish_timestamp) |
