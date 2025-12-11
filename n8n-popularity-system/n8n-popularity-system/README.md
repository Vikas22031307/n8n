# n8n Workflow Popularity System (human style)

This is a small project I built to collect and expose popular n8n workflows from
YouTube, the n8n Discourse forum, and Google Trends. I wrote it quickly, so things
are a bit "real person" in style — small rough edges, pragmatic choices.

Quick summary:
- collectors fetch data from each platform
- SQLite stores the normalized rows
- FastAPI exposes a single `/workflows` endpoint returning JSON
- a cron-job can call the update script regularly

Output JSON shape (exactly this):
{
  "workflow": "string",
  "platform": "YouTube|Forum|Google",
  "popularity_metrics": { /* platform-specific keys */ },
  "country": "US|IN"
}

Quick start:
1. python -m venv venv
2. source venv/bin/activate   # or venv\Scripts\activate on Windows
3. pip install -r requirements.txt
4. copy .env.example to .env and add keys (optional)
5. python data/generate_seed.py   # creates a demo seed file
6. python -m app.update_workflows  # will try to call real APIs if keys set; otherwise no-op collectors
7. uvicorn app.main:app --reload --port 8000

If you want a single-file demo without hitting APIs, run generate_seed.py then
use the small loader script (included) to import the seed into DB before starting the server.
