# Prompt Log — Justin Quinones

**Project:** Security Alert Triage Bot
**Team:** SOC Triagers
**My Component:** Ingestion
**AI Tools Used:** GitHub Copilot, n8n, groq. 

---

## 2026-04-23 — What I was trying to do was trying to use the GitHub Copilot to help me create a README for my component which was the Ingestion component

**Context:** I was on GitHub where I noticed what I had in my component was a little vague and bland and I wanted something that was clear and concise and made sense for the project.

**Prompt:**
> Using the project context from copilot-instructions.md, write a complete README for my [component name] component. Include: What it does (2-3 sentences), How it connects to other components (inputs and outputs), Setup instructions (what accounts/keys are needed, what to configure in n8n/Flowise), How to test it (specific steps) Known limitations

**Result:** The result it gave me was that it generated a table with the "Section" and "Contents" where in the section it includes descriptions such as "What It Does", "How It Connects", "Setup Instructions", "How to Test It", and "Known Limitations". In the "Contents" it includes a description of each.

**Evaluation:** It did work and is almost accurate with the information it provided. What went wrong was the first one with "What It Does", where in the contents, the description did not describe what it does but rather included, "2-sentence overview of the component's role as the entry point."

**What I changed:** What I modified was to give it a summary of what it does and then have it give the 2-sentence overview. 

**What I learned:** What I would do differently would be to give a summary of what the component does that way it can accurately give me a 2-sentence overview next time.

---

## 2026-04-25 — Debugging a Checkpoint 2 Failure

**Context:** While testing the end-to-end pipeline, the AI Core did not update the record status correctly. 

**Prompt:**
> Analyse the AI Core code for analyzing alerts and filling in the correct fields. For some reason while it is analyzing, it doesn't change the status from "new" to "analyzed". Suggest fixes.

**Result:** Copilot was able to recognize what I was talking about and was able to suggest me ways to fix the code so that way it change change the "status" selector in Airtable.

**Evaluation:** The suggestion was accurate and I was able to see how the code could be modified. 

**What I changed:** I personally did not change anything except make note of how it is supposed to look like. Changes will be made by the member responsible for the component. 

**What I learned:** I learned that there is a way that once the Analysis component functions, it can change the status after it is done analyzing the alerts. 

---

## 2026-04-26 — Fixing a Slight Name Mismatch

**Context:** A while ago before doing the checkpoint2-audit and results, I noticed while doing the Ingestion, the JSON payload had used "dst_ip" while the Airtable had expected "destination_ip."

**Prompt:**
> Can you find and correct the field name mismatch between the injection JSON and Airtable schema. 

**Result:** Copilot suggested to me in renaiming the "dst_ip" to "destination_ip" in the ingestion script.

**Evaluation:** I was able to fix it and it worked in an instant. The record now populates correctly. 

**What I changed:** I updated the ingestion script and confirmed the corrected field name in Airtable.

**What I learned:** What I learned was that I had to be precise with the schema so that way I can lessen errors that may occur. 

---

## 2026-04-27 — Generating Test Data for Integration

**Context:** Upon creating test alerts, I realized I needed more detailed realistic records to validate the pipeline

**Prompt:** 
>  Analyze this n8n code node, edit it and give me five realistic cybersecurity alert records for Airtable ingestion, covering normal, edge, and bad data cases.

**Result:** The AI was able to produce a mix of alerts including brute force, malware, lateral movement, data exfiltration, and port scan with varied severities, IPs, and classifications.

**Evaluation:** The data was well-structured and matched my schema perfectly. 

**What I changed:** What I was able to change was adding one malformed IP and one missing destination IP to simulate edge cases. 

**What I learned:** I learned that more realistic alerts are better to have especially for a project. 

---

## 2026-04-28 — Debugging an n8n Expression During End-to-End Flow 

**Context:** The expression used to extract "recommendation" from AI Core output failed during runtime.

**Prompt:** 
>  Can you debug this n8n expression: {{$json["recommendation"]}} returns undefined.

**Result:** AI was able to tell me that the JSON path was nested under data.output.recommendation.

**Evaluation:** Once corrected, the workflow executed successfully.

**What I changed:** What was changed was the expression to {{$json["data"]["output"]["recommendation"]}} and verifies the output.

**What I learned:** I learned not to nest a JSON path in the way that I did because it can generate errors in the future.

---

## 2026-04-29 — Re-Running the Audit Prompt and Comparing Results

**Context:** After fixing several workflow issues, I wanted to confirm readiness for Checkpoint 2.

**Prompt:** 
> Re-run the audit prompt from checkpoint2-audit.md and summarize differences between the first and second runs. 

**Result:** Copilot highlighted that the Ingestion, Analysis, and Monitoring components are fully working while the Action component remails "Partially Working"

**Evaluation:** The comparison was clear and helped finalize my Checkpoint 2 report and for helping me make sure to make the necessary edits.

**What I changed:** What I changed was the audit file and uploaded the necessary screenshots to reflect the improved component statuses.

**What I learned:** I was able to learn was how much change there was between the two comparisons.

---

## 2026-05-02 — Adding Error Handling to Ingestion Workflow

**Context:** The new phase required the workflow to handled malformed input.

**Prompt:** 
> Write for the n8n logic for the ingestion component: if required fields are missing, set status = "error" and add error_reason. 

**Result:** Copilot was able to generate a branch using and IF node and the Airtable setup.

**Evaluation:** It was able to work perfectly where the bad records are now logged instead of dropped. 

**What I changed:** What I changed was when I added the "error reason" field and tested it with a missing IP record.

**What I learned:** I learned that for my component, it is always best to have a workflow that catches errors from within so that it can be filtered out.

---

## 2026-05-03 — Testing Error Path with Bad Data Input

**Context:** I needed this to confirm that the error handling triggers correctly. 

**Prompt:** 
> Generate a test record missing a destination IP to trigger an error path.

**Result:** Copilot produced a valid malformed record where the worflow set the status to "error."

**Evaluation:** In the Airtable database, it shows the error_reason with "Missing destination IP."

**What I changed:** I managed to save a screenshot of that error so that I can submit it in a future assignment.

**What I learned:** I learned that through testing, the worflow will show that there will be an error if something specific is not included.

---

## 2026-05-04 — Designing Confidence-Based Routing Logic

**Context:** Although my component doesn't use confidence scores, it would be helpful to see the logic of it.

**Prompt:** 
> Suggest a routing logic for ingestion based on alert severity: CRITICAL -> immediate notification, LOW -> daily digest.

**Result:** Copilot proposed an IF node for being able to compare severity values. 

**Evaluation:** The implementation was successful and the records route correctly. 

**What I changed:** I set the threshold to "Critical" severity in case for immediate escalation. 

**What I learned:** This can be helpful in order to see the confidence score based on an alert that comes in and that is analyzed. 

---

## 2026-05-06 — Building Error Monitoring Dashboard View

**Context:** I thought it would be helpful to create a seperate dashboard on the side just to see which alerts had an error. 

**Prompt:** 
> Help me design an Airtable view showing all records with status="error" and grouped by source.

**Result:** Copilot suggested grouping by source and sorting by ingested_at.

**Evaluation:** After creating it, the dashboard clearly shows failed records per component.

**What I changed:**  I created the "Error Monitor" view and added a screenshot in order to submit it in an assignment. 

**What I learned:** I learned that it is helpful to have something that shows the many errors that show up so that they can be filtered and fixed. 

---
