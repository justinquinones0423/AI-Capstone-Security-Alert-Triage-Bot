## Status
- [✓] Design complete
- [✓] Sample data prepared
- [✓] Initial implementation
- [✓] Testing
- [✓] Integration with other components
- [✓] Documentation complete

# Ingestion Component

**Owner:** Justin Quinones  
**Component:** 1 of 4

---

## What It Does

The Ingestion component is the entry point for all security alerts into the system. It accepts incoming alert data from various sources (SIEM, firewall, IDS/IPS, cloud logs), normalizes the data into a common schema, and writes the structured record to Airtable for downstream processing by the AI Core, Action, and Monitoring components.

---

## How It Connects to Other Components

### Inputs

| Source | Format | Description |
|--------|--------|-------------|
| External security tools | Python node code | SIEM alerts, firewall logs, IDS notifications |
| Manual test input | JSON | For testing and demo purposes |

### Outputs

| Destination | Field Written | Description |
|-------------|---------------|-------------|
| Airtable — Security Alerts table | `alert_id` | Unique identifier |
| | `source` | Originating system (e.g., "CrowdStrike", "Palo Alto") |
| | `severity` | High, Critical, Medium, Low |
| | `alert_type` | Category (e.g., "Malware Detected", "Brute Force") |
| | `description` | Full alert details |
| | `source_ip` | Origin IP address |
| | `destination_ip` | Target IP address |
| | `timestamp` | When the alert occurred |
| | `raw_payload` | Original unmodified alert data |
| | `status` | Set to "new" (lowercase) |
| | `ingested_at` | Current timestamp |

### Handoff to AI Core

- **Trigger:** Status field = "new"
- **Mechanism:** AI Core queries Airtable for records where `status = "new"`
- **Automation:** Currently manual; scheduled automation to be added

---

## Setup Instructions

### Prerequisites

| Requirement | How to Obtain |
|-------------|----------------|
| n8n account | Sign up at [n8n.io](https://n8n.io) |
| Airtable account | Sign up at [airtable.com](https://airtable.com) |
| Airtable API key | Generate in Airtable Developer settings |
| Base ID | Copy from your Airtable base URL |
| Table ID | Copy from Airtable table URL |

### Airtable Schema Setup

1. Create a new Base in Airtable
2. Create a table named "Security Alerts"
3. Add the following fields:

| Field Name | Type | Options |
|------------|------|---------|
| alert_id | Single line text | — |
| source | Single line text | — |
| severity | Single select | Critical, High, Medium, Low |
| alert_type | Single line text | — |
| description | Long text | — |
| source_ip | Single line text | — |
| destination_ip | Single line text | — |
| timestamp | Date/time | — |
| raw_payload | Long text | — |
| status | Single select | new, in_progress, resolved |
| ingested_at | Date/time | — |

### n8n Workflow Configuration

1. **Create new workflow** in n8n
2. **Add Webhook node** — Configure as POST endpoint
3. **Add Code node (Python)** — Use the following pattern:

```python
import json
from datetime import datetime

# Input: webhook body (JSON)
data = json.loads($json.body)

# Normalize to common schema
record = {
    "alert_id": data.get("alert_id") or f"ALT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
    "source": data.get("source", "unknown"),
    "severity": data.get("severity", "medium"),
    "alert_type": data.get("alert_type", "unknown"),
    "description": data.get("description", ""),
    "source_ip": data.get("source_ip", ""),
    "destination_ip": data.get("destination_ip", ""),
    "timestamp": data.get("timestamp", datetime.now().isoformat()),
    "raw_payload": json.dumps(data),
    "status": "new",
    "ingested_at": datetime.now().isoformat()
}

return record
```

4. **Add Airtable node** — Configure:
   - Operation: Create
   - Table: Security Alerts
   - Mapping: Map Python output fields to Airtable fields

5. **Activate webhook** — Copy the webhook URL for testing

---

## How to Test It

### Step 1: Verify n8n Workflow is Active

1. Open your n8n workflow
2. Confirm the webhook is showing a URL (not "Not activated")
3. Copy the webhook URL

### Step 2: Send a Test Alert

Using curl:

```bash
curl -X POST https://your-n8n-instance.io/webhook/your-hook-id ^
  -H "Content-Type: application/json" ^
  -d "{\"source\": \"test-source\", \"severity\": \"high\", \"alert_type\": \"Brute Force Attack\", \"description\": \"Failed login attempts detected from 192.168.1.100\", \"source_ip\": \"192.168.1.100\", \"destination_ip\": \"10.0.0.5\", \"timestamp\": \"2026-04-26T10:30:00Z\"}"
```

### Step 3: Verify in Airtable

1. Open your Airtable base
2. Check the Security Alerts table
3. Confirm a new record was created with:
   - `status` = "new"
   - All fields populated correctly
   - `ingested_at` = current timestamp

### Step 4: Test Edge Cases

| Test Case | Input Change | Expected Result |
|-----------|--------------|-----------------|
| Missing optional fields | Remove `source_ip`, `destination_ip` | Record created with empty strings |
| Invalid severity | `"severity": "invalid"` | Defaults to "medium" |
| No alert_id provided | Remove `alert_id` | Auto-generates ALT-YYYYMMDDHHMMSS |

---

## Known Limitations

- **Single alert per request** — The current implementation processes one alert per webhook call. To batch ingest, modify the Python code to loop through an array.
- **No deduplication** — If the same alert is sent twice, two records will be created. Consider adding alert_id uniqueness checks.
- **Manual trigger required** — The handoff to AI Core is not yet automated. Currently requires manual execution or scheduled trigger.
- **Limited input validation** — Invalid IP formats, missing required fields, and malformed JSON are not rigorously validated at the ingestion layer.
- **No retry mechanism** — If Airtable write fails, there is no built-in retry or error queue.
- **Webhook URL exposure** — The webhook URL should be protected via n8n authentication or network restrictions in production.

---

## Related Documentation

- [Component 2 — Analysis](../component-2-Analysis/README.md)
- [Component 3 — Action](../component-3-Action/README.md)
- [Component 4 — Monitoring](../component-4-Monitoring/README.md)
- [Airtable Schema](../../docs/proposal.md)
