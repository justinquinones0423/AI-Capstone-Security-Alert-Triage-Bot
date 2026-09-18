# AI-Powered Security Alert Triage Bot

A modular, end-to-end security operations project designed to reduce alert fatigue for SOC analysts by automatically ingesting, analyzing, prioritizing, and escalating security alerts using AI and automation.

This project was built as a capstone-style portfolio system to demonstrate how modern AI, workflow automation, and operational monitoring can work together to support real-world cybersecurity operations.

## Problem

Security operations teams are flooded with alerts from SIEM tools, firewalls, IDS/IPS systems, cloud platforms, and endpoint protection tools. Many of these alerts are low-priority, redundant, or false positives. Analysts often spend hours manually triaging incoming events, which slows response time and increases the risk of missing a real incident.

## Solution

This project creates a workflow where security alerts are:

- ingested from multiple sources,
- normalized into a consistent schema,
- analyzed by AI agents for severity, threat context, and recommended action,
- routed into automated action workflows,
- monitored through a dashboard for operational visibility.

The result is a faster, more consistent triage process that helps analysts focus on the incidents that matter most.

## Architecture Overview

```text
Security Tools / Simulated Alerts
        ↓
[Component 1: Ingestion]
        ↓
Airtable as the operational source of truth
        ↓
[Component 2: AI Analysis]
  - Alert classification
  - Threat research
  - Recommended response
        ↓
[Component 3: Action]
  - Ticket creation
  - Escalation rules
  - Response automation
        ↓
[Component 4: Monitoring]
  - Dashboards
  - Metrics and operational visibility
```

## What the System Does

The system provides a practical AI-assisted triage pipeline for cybersecurity alerts:

- accepts raw alert data via webhook-based ingestion,
- standardizes the fields into a common schema,
- determines whether an alert is likely malicious, benign, or needs human review,
- identifies relevant attack patterns and threat context,
- recommends response actions based on severity and impact,
- creates follow-up tickets or escalation workflows for responders,
- exposes operational metrics through a monitoring dashboard.

## Repository Structure

```text
AI-Capstone-Security-Alert-Triage-Bot/
├── README.md
├── docs/
│   └── proposal.md
├── component-1-Ingestion/
│   └── README.md
├── component-2-Analysis/
│   └── README.md
├── component-3-Action/
│   └── README.md
├── component-4-Monitoring/
│   └── README.md
├── data/
├── weekly-labs/
├── prompt-log-justin.md
├── prompt-log-alexander.md
└── .github/
```

## Component Breakdown

### 1. Ingestion

The ingestion layer is responsible for bringing security alerts into the system. It accepts incoming data from external sources, normalizes it into a common format, and stores it in Airtable for downstream processing.

Key responsibilities:
- webhook intake for alert payloads,
- data standardization,
- alert storage in a structured table,
- status tracking for newly ingested alerts.

Tools used:
- n8n
- Airtable
- Python

### 2. Analysis

The analysis layer uses a multi-agent AI approach to reason about each alert. Different agent roles focus on distinct tasks, such as:
- classifying severity and confidence,
- identifying threat behavior and attack patterns,
- recommending next steps or remediation.

This makes the output more structured, auditable, and actionable than a single monolithic LLM prompt.

Key responsibilities:
- security alert classification,
- threat intelligence-style reasoning,
- recommendation generation,
- structured JSON output for downstream automation.

Tools used:
- n8n
- Google Gemini / LLM APIs
- Python
- JSON-based structured prompting

### 3. Action

The action layer converts triage results into operational response workflows. Based on the severity and analysis findings, the system can create tickets, trigger escalations, or route work to human responders.

Key responsibilities:
- incident ticket creation,
- escalation based on severity,
- workflow automation for response coordination.

Tools used:
- n8n
- ticketing or issue-tracking systems

### 4. Monitoring

The monitoring component provides visibility into the triage workflow. It surfaces metrics like alert volume, severity distribution, and turnaround time so SOC teams can understand performance and operational health.

Key responsibilities:
- dashboard reporting,
- volume and trend analysis,
- triage effectiveness visibility.

Tools used:
- Streamlit
- Airtable
- Python

## Workflow

A typical alert follows this path:

1. A simulated or real security tool sends a raw alert payload.
2. The ingestion workflow receives and normalizes it.
3. The alert is saved in Airtable with a status such as "new".
4. The AI analysis layer evaluates severity, threat type, and recommended actions.
5. The action workflow creates tickets or escalations for higher-risk alerts.
6. The monitoring layer tracks volume, response time, and trend data.

## Tech Stack

- Workflow automation: n8n
- Data layer: Airtable
- AI/LLM: Gemini / structured prompting
- Programming: Python
- Visualization: Streamlit
- Documentation and project planning: GitHub, Markdown

## Why This Project Matters

This project demonstrates how AI can be used in a real operational context, not just as a chatbot or demo. It combines software engineering, automation, and cybersecurity thinking into a practical architecture for handling security events at scale.

It is especially relevant to organizations facing:
- high alert volume,
- limited analyst bandwidth,
- inconsistent manual triage,
- pressure to automate first-pass incident handling.

## Outcomes and Value

This solution aims to:
- reduce response time for critical incidents,
- reduce analyst workload,
- improve consistency in triage decisions,
- provide a foundation for future AI-assisted security workflows,
- create a clear, modular architecture suitable for extension.

## Project Status

The repository is organized as a multi-component capstone project showing a full pipeline from ingestion to action and monitoring. It reflects a realistic systems design approach for AI-enabled security operations.

## Future Improvements

Potential next steps include:
- adding alert deduplication and enrichment,
- expanding threat intelligence integrations,
- improving confidence scoring and escalation logic,
- adding deeper dashboard analytics and historical trend analysis,
- integrating with production security tooling and incident management platforms.

## Summary

This project showcases the design and implementation of an AI-powered security alert triage system that helps organizations automate the front end of incident response. It blends cybersecurity operations, AI reasoning, workflow orchestration, and dashboard monitoring into one cohesive, portfolio-ready solution.

For employers, the project demonstrates:
- systems thinking,
- AI implementation in a real domain,
- workflow automation,
- data handling and integration design,
- security-focused problem solving.
