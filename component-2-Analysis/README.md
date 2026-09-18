  # Component 2: Alert Analysis Engine

  **Owner:** Alexander Lustig

  ## Problem Statement

  SOC analysts are drowning in alerts. A typical SOC generates thousands of alerts per day — most false positives. When
  a real threat arrives, it's buried under noise. Analysts need to quickly determine:
  1. **Is this real?** (severity assessment)
  2. **What is it?** (threat context)
  3. **What do I do?** (recommended action)

  Today, analysts do this manually, reading through alert data and matching patterns against threat intelligence. It's
  slow and error-prone.

  ## Solution: Sequential LLM Pipeline

  This component pulls alert records from Airtable and runs each one through three sequential calls to Groq's
  `llama-3.1-8b-instant`, then writes the results back to the same Airtable base.

  ### Architecture

  Airtable "Alerts" table (populated by Component 1)
       ↓
  Python script (Github to airtable.py) — reads all records
       ↓
  For each alert:
  ┌────────────────────────────────────────┐
  │  Call 1: Analyst prompt                │
  │  "State whether this is a real threat  │
  │   or false positive and why."          │
  │  Output: analyst_notes (free text)     │
  └────────────────────────────────────────┘
       ↓
  ┌────────────────────────────────────────┐
  │  Call 2: Researcher prompt             │
  │  "Add threat intelligence context."    │
  │  (fed the alert + analyst_notes)       │
  │  Output: researcher_notes (free text)  │
  └────────────────────────────────────────┘
       ↓
  ┌────────────────────────────────────────┐
  │  Call 3: Recommender prompt            │
  │  Choose one: Escalate / Monitor / Close│
  │  (fed the alert + both prior notes)    │
  │  Output: recommendation (free text)    │
  └────────────────────────────────────────┘
       ↓
  Heuristic confidence score (code, not the LLM — see below)
       ↓
  PATCH back to the Airtable record

  There is no orchestration layer (no n8n, no queue, no trigger) — the script is a plain `for` loop over every record
  currently in the Airtable table and is invoked manually / on demand. It does not filter by `status`, so re-running it
  reprocesses every record.

  ### Key Design Decisions

  | Decision | Why | Alternative Considered |
  |----------|-----|------------------------|
  | **Three sequential prompts instead of one call** | A single prompt asking for severity + context + action at once
  produced vague, unfocused answers. Chaining three narrow prompts (each fed the prior output) kept each response
  on-task. | Single monolithic prompt |
  | **Groq (`llama-3.1-8b-instant`)** | Fast, free-tier inference, good enough for a capstone prototype. | Gemini /
  OpenAI / Claude — not used in this component |
  | **Airtable as the shared data store** | Matches the project's shared schema so Components 1/3/4 can read the same
  table. | A dedicated database |
  | **Confidence score computed in code, not by the model** | The LLM was never asked for and does not return a
  confidence number. `get_confidence()` derives a proxy score from the recommendation keyword (Escalate/Monitor/Close)
  plus a word-count bonus on the two notes fields. This is a heuristic stand-in, not a calibrated model confidence. |
  Ask the LLM to self-report confidence (not implemented) |
  | **Free-text outputs, not structured JSON** | Prompts ask for prose ("2–3 sentences"), not a JSON schema, and nothing
  parses or validates the responses. | Structured JSON + schema validation (not implemented) |

  ## Implementation

  ### Files

  component-2-Analysis/
  ├── README.md                                        ← you are here
  ├── Airtable to github.py                             ← earlier version (no error handling,
  │                                                          no confidence score — superseded)
  ├── Github to airtable.py                              ← current version: adds per-call error
  │                                                          handling, heuristic confidence score,
  │                                                          and status ("Analyzed"/"In Progress"/"error")
  ├── ALERT.json                                          ← 5 real Airtable records showing actual
  │                                                          pipeline output (see below)
  ├── Co-Pilot Audit                                      ← gap-analysis notes from a checkpoint review
  └── Co-Pilot component-2-multi-agent-explanation.md     ← early design notes for a more ambitious
                                                              multi-agent version that wasn't built

  ### How It Works

  1. `get_alerts()` fetches every record currently in the Airtable `Alerts` table.
  2. For each record, three Groq calls run in sequence (analyst → researcher → recommender), each one receiving the
  alert fields plus whatever the previous call returned.
  3. `get_confidence()` derives a 0–1 score from the recommendation keyword and response length — this is a heuristic,
  not a model output.
  4. The result is written back with `PATCH` to the same Airtable record. In `Github to airtable.py`, a failure at any
  stage is caught, the record is marked `status: "error"` with an `error_reason`, and processing moves to the next alert
  instead of crashing the run.

  ### Actual Sample Output

  `ALERT.json` contains 5 real records that were processed through this pipeline and captured from Airtable — this is
  genuine output, not a mockup:

  | Alert | Type | Input Severity | Recommendation Produced |
  |-------|------|-----------------|--------------------------|
  | alert-001 | brute_force | High | Escalate |
  | alert-002 | Malware in temp directory | Critical | Escalate |
  | alert-003 | Lateral movement | Critical | Escalate |
  | alert-004 | Data exfiltration (2.3GB outbound) | Critical | Escalate |
  | alert-005 | Port scan (internal subnet) | Low | Close |

  Qualitatively, this is the behavior you'd want: the low-severity internal port scan gets closed, everything flagged
  Critical/High gets escalated. This has **not** been run against a larger or adversarial test set, and no
  false-positive/false-negative rate has been measured.

  ## What I Learned

  1. **Sequential prompting compounds early mistakes** — if the analyst call misjudges an alert, the researcher and
  recommender calls inherit that framing since each is fed the prior output. There's no independent second opinion.
  2. **A heuristic confidence score is not the same as a calibrated one** — `get_confidence()` is a reasonable stand-in
  for surfacing *something* to downstream components, but it's derived from keyword matching and word count, not from
  the model's actual certainty.
  3. **Free-text LLM output without a schema is fragile for downstream consumers** — nothing here validates that
  `recommendation` actually starts with Escalate/Monitor/Close; it's just checked with `in` string matching.
  4. **Hardcoded API keys in a script are a real liability** — an earlier version of this file had a live Groq key and
  Airtable token committed in plaintext. Secrets belong in environment variables, not source, full stop — especially in
  a public repo for a *security* project.
  5. **No trigger/filter logic means the script isn't idempotent** — running it twice reprocesses every alert in the
  table, since there's no `status == "new"` check before pulling records.

  ## Known Limitations (not yet built)

  - No accuracy, latency, or token-cost benchmarking has been done — any such numbers would be invented, so none are
  published here.
  - No MITRE ATT&CK mapping — the researcher prompt asks for general "threat intelligence context," not technique IDs.
  - No n8n or workflow-engine orchestration — this is a script, not a triggered pipeline.
  - No structured/validated output format.
  - No automated test suite or held-out evaluation set beyond the 5 records in `ALERT.json`.

  ## Integration Points

  - **Ingestion (Component 1):** writes alert records into the shared Airtable `Alerts` table this script reads from.
  - **Action (Component 3):** would read `recommendation` / `status` from Airtable to drive downstream response — not
  yet built by the team.
  - **Monitoring (Component 4):** would read the `status`/error fields this script writes — not yet built by the team.

  ## Future Improvements

  - Move `GROQ_API_KEY` / `AIRTABLE_TOKEN` to environment variables (already partially done in `Github to airtable.py`,
  which uses a placeholder instead of a real key inline — but the raw key still needs to be rotated and scrubbed from
  git history in the earlier file).
  - Filter `get_alerts()` by `status` so reruns don't reprocess everything.
  - Ask the model for structured JSON and validate it, instead of parsing prose with keyword matching.
  - Replace the heuristic confidence score with something calibrated (e.g., log-probabilities if the provider exposes
  them, or a labeled evaluation set to check keyword-based confidence against real outcomes).
  - Build an actual evaluation set (a batch of labeled alerts with known correct severity/action) and measure real
  accuracy/latency/cost — none of that exists yet.
