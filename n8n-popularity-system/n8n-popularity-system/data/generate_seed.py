import json, random, os
OUT = "seed_workflows.json"
N = 60
COUNTRIES = ["US", "IN"]
YT_TITLES = [
    "Automating Gmail with n8n",
    "Google Sheets → Slack Automation with n8n",
    "n8n Slack integration tutorial",
    "n8n WhatsApp reminders flow",
    "n8n Notion automation example",
    "n8n Airtable sync demo",
    "n8n Gmail filter and reply",
    "n8n Trello board automation"
]
FORUM_TITLES = [
    "WhatsApp reminders workflow",
    "n8n + Google Sheets: best practice",
    "Anyone used n8n with Notion?",
    "How to build a Slack bot with n8n",
    "n8n + Airtable sync issues",
    "n8n Gmail webhook problems",
    "Scheduling flows with n8n"
]
KW = [
    "n8n slack integration",
    "n8n gmail automation",
    "n8n google sheets integration",
    "n8n whatsapp reminders",
    "n8n notion automation"
]

items = []
for i in range(N):
    kind = random.choice(["YouTube", "Forum", "Google"])
    country = random.choice(COUNTRIES)
    if kind == "YouTube":
        title = random.choice(YT_TITLES)
        views = random.randint(1000, 50000)
        likes = random.randint(10, max(20, int(views * 0.05)))
        comments = random.randint(0, max(5, int(views * 0.01)))
        items.append({
            "workflow": title + (f" ({i})" if random.random() < 0.1 else ""),
            "platform": "YouTube",
            "country": country,
            "popularity_metrics": {
                "views": views,
                "likes": likes,
                "comments": comments,
                "like_to_view_ratio": round(likes / views, 4) if views else None,
                "comment_to_view_ratio": round(comments / views, 4) if views else None
            }
        })
    elif kind == "Forum":
        title = random.choice(FORUM_TITLES)
        views = random.randint(200, 8000)
        likes = random.randint(0, 200)
        comments = random.randint(0, 200)
        items.append({
            "workflow": title + (f" ({i})" if random.random() < 0.2 else ""),
            "platform": "Forum",
            "country": country,
            "popularity_metrics": {
                "views": views,
                "likes": likes,
                "comments": comments,
                "replies": comments,
                "unique_contributors": random.randint(1, min(20, comments+1))
            }
        })
    else:
        kw = random.choice(KW)
        monthly = random.randint(100, 5000)
        change = round(random.uniform(-30.0, 120.0), 1)
        items.append({
            "workflow": kw,
            "platform": "Google",
            "country": country,
            "popularity_metrics": {
                "monthly_search_volume": monthly,
                "change_last_60_days": change
            }
        })

os.makedirs(os.path.dirname(__file__), exist_ok=True)
with open(os.path.join(os.path.dirname(__file__), OUT), "w", encoding="utf-8") as f:
    json.dump(items, f, indent=2)

print(f"Generated {len(items)} items -> {os.path.join(os.path.dirname(__file__), OUT)}")
