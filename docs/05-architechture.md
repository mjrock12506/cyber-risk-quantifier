# Architecture — Cyber Risk Quantifier

## System Diagram (text)
## Deployment Flow
1. Developer runs `git push` from local machine
2. GitHub receives push on `main` branch
3. GitHub webhook notifies Streamlit Cloud
4. Streamlit Cloud pulls new code, rebuilds Python environment from `requirements.txt`
5. New app version live within ~60 seconds
6. No downtime (Streamlit Cloud blue/green deploys)

## Data Architecture
No persistent data. Every session is independent. User inputs live in `st.session_state`
during the browser session; discarded on page close.

## Future-State (v2+)
- Add Redis session store for multi-page workflows
- Add Postgres for saved scenarios (requires authentication)
- Add Celery worker for long-running batch simulations