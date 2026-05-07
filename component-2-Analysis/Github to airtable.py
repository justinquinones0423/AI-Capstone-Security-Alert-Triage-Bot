import requests
import json

GROQ_API_KEY = "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"
AIRTABLE_TOKEN = "pat4TEKjHaDy6fXyi.3a2449a91eb923c1c6509eac28b0e78e59479f498af8ee583b940cef16cc1858"
BASE_ID = "appdNv0F6L4BbHMDb"
TABLE_NAME = "Alerts"

GROQ_HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

AIRTABLE_HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}",
    "Content-Type": "application/json"
}

def ask_groq(prompt):
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=GROQ_HEADERS,
            json=data,
            timeout=30
        )
        if response.status_code != 200:
            return None, f"API error: {response.status_code}"
        result = response.json()
        if "error" in result:
            return None, f"Error: {result['error']}"
        return result["choices"][0]["message"]["content"], None
    except Exception as e:
        return None, f"Error: {str(e)}"

def get_confidence(recommendation):
    if "Escalate" in recommendation:
        return 0.9
    elif "Monitor" in recommendation:
        return 0.6
    elif "Close" in recommendation:
        return 0.8
    else:
        return 0.5

def get_alerts():
    response = requests.get(
        f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}",
        headers=AIRTABLE_HEADERS
    )
    return response.json().get("records", [])

def update_airtable(record_id, analyst, researcher, recommendation, confidence=None, error=None):
    if error:
        data = {
            "fields": {
                "status": "error",
                "error_reasoning": error
            }
        }
    else:
        status = "analyzed" if confidence > 0.7 else "needs_review"
        data = {
            "fields": {
                "analyst_notes": analyst,
                "researcher_notes": researcher,
                "recommendation": recommendation,
                "confidence_rating": confidence,
                "status": status
            }
        }

    response = requests.patch(
        f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}/{record_id}",
        headers=AIRTABLE_HEADERS,
        json=data
    )
    if response.status_code == 200:
        print(f"✅ {record_id} updated")
    else:
        print(f"❌ Failed: {response.status_code}")

alerts = get_alerts()
print(f"Found {len(alerts)} alerts. Processing...")

for alert in alerts:
    fields = alert["fields"]
    record_id = alert["id"]

    alert_text = (
        f"Alert ID: {fields.get('alert_id')} | "
        f"Type: {fields.get('alert_type')} | "
        f"Severity: {fields.get('severity')} | "
        f"Source IP: {fields.get('source_ip')} | "
        f"Description: {fields.get('description')}"
    )

    print(f"Processing {fields.get('alert_id')}...")

    analyst, analyst_err = ask_groq(
        f"You are a SOC analyst. In 2-3 sentences, state whether this is a real threat or false positive and why.\nAlert: {alert_text}"
    )
    if analyst_err:
        print(f"  ❌ {analyst_err}")
        update_airtable(record_id, "", "", "", error=analyst_err)
        continue

    researcher, researcher_err = ask_groq(
        f"You are a threat researcher. In 2-3 sentences, add threat intelligence context.\nAlert: {alert_text}\nAnalyst: {analyst}"
    )
    if researcher_err:
        print(f"  ❌ {researcher_err}")
        update_airtable(record_id, analyst, "", "", error=researcher_err)
        continue

    recommendation, rec_err = ask_groq(
        f"""You are a senior security advisor. Choose exactly one action:
- Escalate: confirmed real threat, high severity, needs immediate response
- Monitor: suspicious but unconfirmed, low/medium severity, needs watching
- Close: false positive, no credible threat

Respond with exactly one word (Escalate, Monitor, or Close) then one sentence explaining why.
Alert: {alert_text}
Analyst: {analyst}
Researcher: {researcher}"""
    )
    if rec_err:
        print(f"  ❌ {rec_err}")
        update_airtable(record_id, analyst, researcher, "", error=rec_err)
        continue

    confidence = get_confidence(recommendation)
    print(f"  Confidence: {confidence}")
    update_airtable(record_id, analyst, researcher, recommendation, confidence)

print("Done.")
