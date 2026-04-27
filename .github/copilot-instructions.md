# Capstone Project Context
## Project

- **Name:** Security Alert Triage Bot
- **Team:** Justin Quinones - Ingestion, Alexander Lustig - Analysis, Ujjwal Singh - Action, Abdoul Sawadogo - Monitoring
- **What it does:** Through the ingestion component, the alerts are created through the n8n code node using python (using a webhook to call in alerts could not be done due to time constraints), then those alerts are updated through the airtable update node in real time and are classified in different fields. In the analysis component, 3 AI models are used to analyze and evaluate the alerts and provides 3 additional types of analysis which are recommendation, analysis_notes and researcher_notes. Through the action component, after the AI analysis is done, there is an n8n workflow that checks the alerts and creats a ticket based on each alert that was analyzed. Finally, in the monitoring component, a dashboard is created through Streamlit to  show triage volume, severity distribution, and response time metrics.
- **Project type:** SOC alert triage assistant for security analysts, designed to automate the initial analysis and prioritization of security alerts, providing actionable insights and recommendations to help analysts focus on the most critical threats.

## Architecture
- **Ingestion:** Based on the ingestion component, the data is stored in the form of a python code that is stored inside a code node that calls the alerts and once it does that, there is an update Airtable node that updates the database with the alerts that were called.
- **AI Core:** Within the second component, there are 3 different AI models including Groq that analyses the alerts and provides classifications with explanation as well.
- **Specialist:** After having the AI models analyze each alert, there is another n8n workflow that does a scan for the alerts and creates a ticket for the alerts. 
- **Integration:** After the 3 components do their job and connect, the final component of Monitoring connects everything through displaying the alerts through a dashboard in Streamlit for viewing.

## Tech Stack
- n8n Cloud (workflow automation)
- Groq API (LLM inference — llama-3.3-70b-versatile)
- Hugging Face Inference API (sentiment analysis, NER, zero-shot classification)
- Airtable (shared database — [1] table)
- GitHub (repo, documentation, portfolio)

## Airtable Schema


### [Security Alerts Table]
| Field | Type | Written By | Status Values |
|-------|------|-----------|---------------|
| alert_id | single_line_text | Ingestion | - |
| source | single_line_text | Ingestion | - |
| severity | single_select | Ingestion | High, Critical, Medium, Low |
| alert_type | single_line_text | Ingestion | - |
| description | long_text | Ingestion | - |
| source_ip | single_line_text | Ingestion | - |
| destination_ip | single_line_text | Ingestion | - |
| timestamp | date_time | Ingestion | - |
| raw_payload | long_text | Ingestion | - |
| status | single_select | Ingestion | New, In Progress, Resolved |
| ingested_at | date_time | Ingestion | - |
| recommendation | long_text | Analysis | - |
| analysis_notes | long_text | Analysis | - |
| researcher_notes | long_text | Analysis | - |
| ticked_url | single_line_text | Action | - |

## Conventions
- Field names: snake_case
- Status values: lowercase
- Date fields end in _at
- Boolean fields use is_ prefix
- Primary key: alert_id 
- Severity levels: high, critical, medium, low

## Current State
- **What's working:** What is already built and tested was the n8n workflow for the Ingestion component for the two nodes. What was also already built and tested was the AI models for analysis in the second component and also the fourth component with the dashboard that was also tested and built.  
- **What's in progress:** What is currently being built right now is the n8n workflow for the third component that is still needed. 
- **Known issues:** The only problem we had was creating the webhook for the first component. The webhook would function but it would only call one alert instead of all of them.
- **Next milestone:** Checkpoint 2 (Week 9) — one record end-to-end through all components.

## Repository Structure
AI-Capstone-Security-Alert-Triage-Bot/
├── README.md
├── component-1-Ingestion/
│   └── README.md
├── component-2-Analysis/
│   └── README.md
├── component-3-Action/
│   └── README.md
├── component-4-Monitoring/
│   └── README.md
├── data/
│   └── README.md
├── docs/
│   └── proposal.md
└── weekly-labs/
    ├── week-04-model-comparison/
    │   ├── README.md
    │   ├── report.md
    │   └── results/
    │       └── comparison-table.csv
    └── week-05-automl-training/
        ├── metrics/
        │   └── confusion-matrix.md
        ├── results/
        │   └── comparison-table.csv
        └── teachable-machine/
            └── screenshots/