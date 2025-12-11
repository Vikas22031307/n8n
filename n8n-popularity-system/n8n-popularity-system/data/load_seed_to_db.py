import json, os
from app.database import Base, engine, SessionLocal
from app.crud import upsert_workflow

Base.metadata.create_all(bind=engine)
db = SessionLocal()

path = os.path.join(os.path.dirname(__file__), "seed_workflows.json")
if not os.path.exists(path):
    print("seed file not found. run generate_seed.py first.")
    exit(1)

items = json.load(open(path, "r", encoding="utf-8"))
for it in items:
    wf = {
        "workflow": it.get("workflow"),
        "platform": it.get("platform"),
        "country": it.get("country"),
    }
    metrics = it.get("popularity_metrics", {})
    wf.update(metrics)
    wf["extra"] = {"seed": True}
    upsert_workflow(db, wf)
print("Imported seed into DB.")
