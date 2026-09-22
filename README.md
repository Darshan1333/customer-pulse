# Customer Pulse — Hunar.AI Assignment

## What it is
Customer Pulse is a lightweight Customer Intelligence Tool for Customer Success Managers. It turns account health, product usage, stakeholder context, company signals and risks into a concise pre-call briefing.

## Core problem
CSMs often have customer data in multiple places and spend too much time assembling context before a customer conversation. The tool answers two questions:
1. What is happening inside my customer's organisation?
2. What useful insight can I share with the customer today?

## Key assumptions
- A production version would connect to CRM, product analytics, support/ticketing and trusted external company/news sources.
- Customer-specific data would be permissioned and refreshed automatically.
- AI would summarize and prioritize signals rather than replace the CSM's judgment.
- Demo data is included so the reviewer can test the workflow without credentials or external API keys.

## Solution design
1. Customer selection establishes the account context.
2. KPI layer gives a fast health/adoption/renewal snapshot.
3. Signal layer surfaces company, leadership, product-usage and support changes.
4. Insight layer converts those signals into a customer-relevant talking point.
5. Risk layer links risks to a concrete next action.
6. Stakeholder layer keeps the CSM aware of the people who matter.
7. Action plan converts intelligence into preparation, engagement and follow-through.

## Why this is useful
The design deliberately avoids becoming a generic news dashboard. The output is action-oriented: every meaningful signal is translated into "why it matters" and "what should the CSM do next?"

## Local run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deployment
This app is ready for Streamlit Community Cloud or any environment that can run Streamlit. No API keys are required for the demo version.

## Suggested production roadmap
- CRM integration (HubSpot/Salesforce)
- Product usage integration
- Support-ticket integration
- Company/news data sources
- AI summarization with source citations
- Automated account-health scoring
- Slack/email daily briefing
- Audit trail for insights and CSM actions
