from typing import List, Dict
import requests
from ..config import DISCOURSE_BASE_URL, DISCOURSE_API_KEY, DISCOURSE_API_USERNAME, COUNTRIES
import time

HEADERS = {}
if DISCOURSE_API_KEY and DISCOURSE_API_USERNAME:
    HEADERS = {"Api-Key": DISCOURSE_API_KEY, "Api-Username": DISCOURSE_API_USERNAME}

def collect_forum_workflows() -> List[Dict]:
    url = f"{DISCOURSE_BASE_URL}/latest.json"
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        r.raise_for_status()
        payload = r.json()
    except Exception as e:
        print("[forum] error fetching latest.json:", e)
        return []

    topics = payload.get("topic_list", {}).get("topics", [])
    out = []

    for t in topics:
        title = t.get("title", "").strip()
        if "n8n" not in title.lower():
            continue

        topic_id = t.get("id")
        views = t.get("views", 0)
        reply_count = t.get("reply_count", 0)
        like_count = t.get("like_count", 0)

        uniq = None
        if topic_id:
            try:
                det = requests.get(f"{DISCOURSE_BASE_URL}/t/{topic_id}.json", headers=HEADERS, timeout=12).json()
                participants = det.get("details", {}).get("participants", [])
                uniq = len(participants)
            except Exception:
                uniq = None
            time.sleep(0.15)

        for country in COUNTRIES:
            out.append({
                "workflow": title,
                "platform": "Forum",
                "country": country,
                "views": views,
                "likes": like_count,
                "comments": reply_count,
                "replies": reply_count,
                "unique_contributors": uniq,
                "like_to_view_ratio": (float(like_count) / views) if views else None,
                "comment_to_view_ratio": (float(reply_count) / views) if views else None,
                "extra": {"topic_id": topic_id, "url": f"{DISCOURSE_BASE_URL}/t/{topic_id}"}
            })

    return out
