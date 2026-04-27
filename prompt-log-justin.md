# Prompt Log — Justin Quinones

**Project:** Security Alert Triage Bot
**Team:** SOC Triagers
**My Component:** Ingestion
**AI Tools Used:** GitHub Copilot, n8n, groq. 

---

## How to Use This Log

Add an entry for each significant AI interaction:
- Copilot Chat conversations where you asked it to generate, explain, or debug
something
- Moments where Copilot was wrong and you had to fix it (these are the most valuable
entries)
- Cases where you refined a prompt to get a better result

Don't log: every autocomplete of a bracket or variable name.

---

## 2026-04-23 — What I was trying to do was trying to use the GitHub Copilot to help me create a README for my component which was the Ingestion component.

**Context:** I was on GitHub where I noticed what I had in my component was a little vague and bland and I wanted something that was clear and concise and made sense for the project.

**Prompt:**
> Using the project context from copilot-instructions.md, write a complete README for my [component name] component. Include: What it does (2-3 sentences), How it connects to other components (inputs and outputs), Setup instructions (what accounts/keys are needed, what to configure in n8n/Flowise), How to test it (specific steps) Known limitations

**Result:** The result it gave me was that it generated a table with the "Section" and "Contents" where in the section it includes descriptions such as "What It Does", "How It Connects", "Setup Instructions", "How to Test It", and "Known Limitations". In the "Contents" it includes a description of each.

**Evaluation:** It did work and is almost accurate with the information it provided. What went wrong was the first one with "What It Does", where in the contents, the description did not describe what it does but rather included, "2-sentence overview of the component's role as the entry point."

**What I changed:** What I modified was to give it a summary of what it does and then have it give the 2-sentence overview. 

**What I learned:** What I would do differently would be to give a summary of what the component does that way it can accurately give me a 2-sentence overview next time.