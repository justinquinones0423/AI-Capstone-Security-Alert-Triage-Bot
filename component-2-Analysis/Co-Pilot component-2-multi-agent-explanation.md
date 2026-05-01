I'll provide a comprehensive explanation of how the Analysis component's multi-agent system works based on your capstone project context.

## Analysis Component: Multi-Agent System Architecture

### 1. **What Each Agent Does**

#### **Analyst Agent** — Severity & Confidence Assessment
- **Purpose:** Determines the threat level and conviction of the classification
- **Input:** Raw alert text from Component 1 (Ingestion)
- **Output:** 
  - `severity`: LOW, MEDIUM, HIGH, or CRITICAL
  - `confidence`: 0-1 confidence score
- **Logic:** Evaluates urgency, impact scope, and immediacy of threat
- **Example reasoning:** "This alert shows repeated failed login attempts to a privileged account within 5 minutes. High severity due to potential account compromise. Confidence: 0.92"

---

#### **Researcher Agent** — Attack Intelligence & IOCs
- **Purpose:** Identifies what type of attack is occurring and extracts indicators of compromise
- **Input:** Alert text + severity/confidence from Analyst Agent
- **Output:**
  - `attack_type`: brute force, phishing, C2 communication, insider threat, etc.
  - `indicators`: JSON array of IOCs (IP addresses, domains, file hashes, email addresses)
- **Logic:** Pattern matching against known attack signatures and threat intelligence
- **Example reasoning:** "Pattern matches brute force attack. Extracted IOCs: [attacker_ip: 192.168.1.100, target_account: admin, protocol: SSH, attempts: 47]"

---

#### **Recommender Agent** — Impact & MITRE ATT&CK Mapping
- **Purpose:** Assesses business impact and maps attack to MITRE ATT&CK framework
- **Input:** Alert text + attack type from Researcher Agent
- **Output:**
  - `potential_impact`: Worst-case scenario description
  - `mitre_techniques`: JSON array of related ATT&CK techniques (e.g., T1110 - Brute Force)
- **Logic:** Maps attack patterns to MITRE framework for standardized threat classification
- **Example reasoning:** "Attack aligns with MITRE T1110.001 (Password Guessing). Potential impact: Unauthorized access to admin account could lead to lateral movement and data exfiltration."

---

### 2. **How They Work Together**

```
┌─────────────────────────────────────────────────────────────┐
│                    RAW ALERT (Component 1)                  │
│         "Multiple failed SSH login attempts detected        │
│          to admin@server.com from 192.168.1.100            │
│          within 5 minutes, 47 attempts total"              │
└──────────────────────────────┬──────────────────────────────┘
                               │
                ┌──────────────▼──────────────┐
                │   ANALYST AGENT             │
                │ • Evaluates severity        │
                │ • Assesses confidence       │
                └──────────────┬──────────────┘
                               │
                    ┌──────────▼─────────┐
                    │ severity: HIGH     │
                    │ confidence: 0.92   │
                    └──────────┬─────────┘
                               │
                ┌──────────────▼──────────────┐
                │   RESEARCHER AGENT          │
                │ • Identifies attack type    │
                │ • Extracts IOCs             │
                └──────────────┬──────────────┘
                               │
                  ┌────────────▼────────────┐
                  │ attack_type: brute_force│
                  │ indicators: [IOCs...]   │
                  └────────────┬────────────┘
                               │
                ┌──────────────▼──────────────┐
                │  RECOMMENDER AGENT          │
                │ • Assesses business impact  │
                │ • Maps MITRE techniques     │
                └──────────────┬──────────────┘
                               │
              ┌────────────────▼────────────────┐
              │ mitre_techniques: [T1110.001...]│
              │ potential_impact: "Unauthorized │
              │  access could lead to lateral   │
              │  movement and data exfil"      │
              └────────────────┬────────────────┘
                               │
              ┌────────────────▼────────────────┐
              │  ENRICHED ALERT to Airtable    │
              │  (alerts_analyzed table)       │
              └────────────────────────────────┘
```

**Sequential Processing Model:**
1. Alert arrives → Analyst evaluates and produces severity + confidence
2. Analyst output → Researcher refines with attack type + IOCs
3. Researcher output → Recommender maps to MITRE + impact
4. All findings + reasoning trace → Written to Airtable
5. Ready for Component 3 (Action) to consume

---

### 3. **Data Flow Between Agents**

| **Flow Stage** | **Data Passed** | **From** | **To** | **Added Value** |
|---|---|---|---|---|
| 1 | Alert text | Ingestion → Analyst | Analyst | Raw input |
| 2 | Severity + Confidence | Analyst → Researcher | Researcher | Context for attack classification |
| 3 | Attack type + IOCs | Researcher → Recommender | Recommender | Pattern to match against MITRE |
| 4 | Complete enriched alert | All agents → Airtable | alerts_analyzed table | Decision artifact with full reasoning |

**Key Fields in Airtable:**
```json
{
  "alert_id": "INC-20260501-001",
  "alert_text": "[original from Component 1]",
  "severity": "HIGH",           // Analyst output
  "confidence": 0.92,           // Analyst output
  "attack_type": "brute_force", // Researcher output
  "indicators": "[{\"type\": \"ip\", \"value\": \"192.168.1.100\"}, ...]", // Researcher output
  "mitre_techniques": "[{\"id\": \"T1110.001\", \"name\": \"Password Guessing\"}, ...]", // Recommender output
  "potential_impact": "Unauthorized access to admin account...", // Recommender output
  "reasoning": "[Full decision trace from all three agents]", // Audit trail
  "status": "analyzed",
  "created_at": "2026-05-01"
}
```

---

### 4. **Real-World Alert Processing Example**

#### **Scenario: SSH Brute Force Attack**

**Step 1: Raw Alert Ingestion**
```
ALERT RECEIVED:
"IDS detected 47 failed SSH login attempts to admin@mail.internal.com 
from source IP 203.0.113.45 between 14:32-14:37 UTC. 
Attempt pattern: 9 attempts/min with varying credentials."
```

---

**Step 2: Analyst Agent Processing**
```
ANALYSIS:
✓ Severity Indicators:
  - Targeted account: ADMIN (high-privileged)
  - Attack velocity: 9 attempts/minute (aggressive)
  - Duration: 5 minutes (sustained effort)
  - Success rate: 0 (0/47 attempts succeeded - good!)

✓ Output:
  severity: "HIGH"
  confidence: 0.94
  reasoning: "Sustained brute force against admin account is HIGH priority. 
  High confidence due to clear pattern signature."
```

---

**Step 3: Researcher Agent Processing**
```
INPUT RECEIVED FROM ANALYST:
  severity: HIGH, confidence: 0.94

ANALYSIS:
✓ Attack Type Classification:
  - Pattern matches: Brute force password attack
  - Indicators found:
    * Attacker IP: 203.0.113.45 (may be compromised proxy)
    * Target: admin@mail.internal.com
    * Protocol: SSH (port 22)
    * Attack tool signature: None detected (manual or script)
    * Attempt count: 47
    * Time window: 300 seconds

✓ Output:
  attack_type: "brute_force"
  indicators: [
    {"type": "source_ip", "value": "203.0.113.45", "severity": "high"},
    {"type": "username", "value": "admin", "severity": "high"},
    {"type": "service", "value": "SSH", "port": 22},
    {"type": "attack_pattern", "value": "credential_guessing"}
  ]
  reasoning: "Textbook brute force. Extracted 4 key IOCs for threat hunting."
```

---

**Step 4: Recommender Agent Processing**
```
INPUT RECEIVED FROM RESEARCHER:
  attack_type: brute_force
  indicators: [203.0.113.45, admin@mail.internal.com, SSH, ...]

ANALYSIS:
✓ Business Impact Assessment:
  - If compromised: Admin account = full system access
  - Potential lateral movement to: Email, file servers, databases
  - Data at risk: Customer data, intellectual property
  - Compliance impact: GDPR, PCI-DSS notifications

✓ MITRE ATT&CK Mapping:
  - Tactic: Initial Access
  - Technique: T1110 (Brute Force)
    - Sub-technique: T1110.001 (Password Guessing)
    - Sub-technique: T1110.003 (Password Spraying)

✓ Output:
  mitre_techniques: [
    {
      "id": "T1110.001",
      "name": "Password Guessing",
      "tactic": "Initial Access",
      "url": "https://attack.mitre.org/techniques/T1110/001"
    }
  ]
  potential_impact: "Successful compromise of admin account would grant 
  attacker full system access, enabling data theft, system destruction, 
  or lateral movement to critical infrastructure."
  
  reasoning: "SSH brute force against privileged account is HIGH impact. 
  Maps to MITRE T1110.001. Recommend immediate response: block source IP, 
  enable MFA on admin account, review recent SSH logs."
```

---

**Step 5: Final Airtable Record**
```json
{
  "alert_id": "INC-20260501-042",
  "alert_text": "IDS detected 47 failed SSH login attempts to admin@mail.internal.com from source IP 203.0.113.45 between 14:32-14:37 UTC. Attempt pattern: 9 attempts/min with varying credentials.",
  "severity": "HIGH",
  "confidence": 0.94,
  "attack_type": "brute_force",
  "indicators": "[{\"type\": \"source_ip\", \"value\": \"203.0.113.45\", \"severity\": \"high\"}, {\"type\": \"username\", \"value\": \"admin\", \"severity\": \"high\"}, {\"type\": \"service\", \"value\": \"SSH\", \"port\": 22}]",
  "mitre_techniques": "[{\"id\": \"T1110.001\", \"name\": \"Password Guessing\", \"tactic\": \"Initial Access\"}]",
  "potential_impact": "Successful compromise of admin account would grant attacker full system access, enabling data theft, system destruction, or lateral movement to critical infrastructure.",
  "reasoning": "ANALYST: HIGH severity due to admin account targeting + 9 attempts/min over 5 min. RESEARCHER: Brute force pattern confirmed. IOCs extracted: 203.0.113.45, admin account, SSH. RECOMMENDER: HIGH impact - admin compromise = full system access. Maps to MITRE T1110.001.",
  "status": "analyzed",
  "created_at": "2026-05-01"
}
```

---

**Step 6: Handoff to Component 3 (Action)**
Component 3 (Response & Action) now receives this enriched alert and can:
- Auto-block IP 203.0.113.45 based on HIGH severity
- Trigger MFA requirement for admin account
- Create incident ticket with full context
- Send SOC analyst notification with recommended response

---

## Summary

The multi-agent system works by **sequential refinement**:
- **Analyst** answers: *"How bad is this?"* (severity + confidence)
- **Researcher** answers: *"What's the attack?"* (type + IOCs)
- **Recommender** answers: *"What's at stake?"* (impact + MITRE mapping)

Together, they transform raw, unstructured alert text into **rich, actionable security intelligence** that Component 3 can execute on, and that SOC analysts can trust and act upon confidently.
