# Capstone Project Context — GitHub Copilot Instructions

## Project Overview
- **Name:** AI-Powered Security Alert Triage Bot
- **Problem:** SOC analysts overwhelmed by alert volume
- **Solution:** Automated triage system that classifies and prioritizes critical security alerts
- **Team:** Justin Quinones, Alexander Lustig
- **My Component:** Component 2 - Analysis

## Component 2: Analysis

**What it does:** Takes ingested alerts and analyzes them using AI to determine severity, threat type, indicators, and relevant attack techniques.

**Input:** Raw alert records from Component 1 (Ingestion)

**Output:** Enriched alert data with:
- Severity classification (LOW, MEDIUM, HIGH, CRITICAL)
- Confidence score (0-1)
- Attack type (brute force, phishing, C2, etc)
- Key indicators of compromise (IOCs)
- Related MITRE ATT&CK techniques
- Impact assessment

**Status:** ✅ DONE - Multi-agent system with analyst, researcher, and recommender agents. Decision reasoning visible in UI.

## Technology Stack

- **LLM Chains:** Flowise Cloud (https://cloud.flowiseai.com)
- **LLM Model:** Groq llama-3.3-70b-versatile
- **Data Sync:** Python scripts (github_to_airtable.py, airtable_to_github.py)
- **Database:** Airtable (shared base)
- **Data Format:** JSON alert objects

## Airtable Schema (Analysis Component)

### alerts_analyzed (Analysis input/output table)
| Field | Type | Source | Purpose |
|-------|------|--------|---------|
| alert_id | Single line text | Ingestion | Unique identifier from ingested alert |
| alert_text | Long text | Ingestion | Full alert description |
| severity | Single select | Analysis AI | LOW / MEDIUM / HIGH / CRITICAL |
| confidence | Number (0-1) | Analysis AI | Confidence in classification |
| attack_type | Single line text | Analysis AI | Type of threat (brute force, phishing, C2, insider) |
| indicators | Long text | Analysis AI | Key IOCs and threat indicators (JSON array) |
| mitre_techniques | Long text | Analysis AI | Related ATT&CK techniques (JSON array) |
| potential_impact | Long text | Analysis AI | Worst-case impact description |
| reasoning | Long text | Analysis AI | Multi-agent reasoning trace |
| status | Single select | [varies] | analyzing / analyzed / awaiting_response |
| created_at | Date | Analysis | Timestamp of analysis |

## How Analysis Works

1. **Alert Ingestion** → Alert comes in from Component 1
2. **Multi-Agent Analysis:**
   - **Analyst Agent:** Classifies severity and confidence
   - **Researcher Agent:** Identifies attack type and IOCs
   - **Recommender Agent:** Assesses impact and suggests MITRE techniques
3. **Output to Airtable:** All findings stored in alerts_analyzed table
4. **Handoff to Component 3:** Analyzed data ready for Action component

## Current Implementation

- Multi-agent system with reasoning trace
- Processes alerts using Groq LLM
- Syncs data bidirectionally with Airtable
- JSON-based data format for compatibility

## Checkpoint 2 Status

✅ Component 2 is DONE and working. Ready for end-to-end testing with Components 1, 3, and 4.

## Using This File

When asking me (Copilot) for help:
- Reference the Airtable schema fields above
- Mention the multi-agent system structure
- Describe inputs/outputs in terms of the alerts_analyzed table
- Share specific alert examples or errors

Example prompts:
- "Write a comprehensive README for my Analysis component"
- "Generate test alerts in JSON format for my component"
- "Debug this Python script that syncs to Airtable"
