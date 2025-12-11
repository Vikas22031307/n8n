from typing import List, Dict
from googleapiclient.discovery import build
from ..config import YOUTUBE_API_KEY, YOUTUBE_SEARCH_TERMS, COUNTRIES
import time

def safe_ratio(a, b):
    try:
        if a is None or b is None or b == 0:
            return None
        return float(a) / float(b)
    except:
        return None

def collect_youtube_workflows() -> List[Dict]:
    if not YOUTUBE_API_KEY:
        print("[youtube] no API key set; skipping YouTube collection")
        return []

    yt = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    out = []

    for country in COUNTRIES:
        for query in YOUTUBE_SEARCH_TERMS:
            try:
                sresp = yt.search().list(
                    part="snippet",
                    q=query,
                    type="video",
                    regionCode=country,
                    maxResults=25
                ).execute()
            except Exception as e:
                print("[youtube] search error:", e)
                time.sleep(1)
                continue

            video_ids = [item["id"]["videoId"] for item in sresp.get("items", []) if item.get("id", {}).get("videoId")]
            if not video_ids:
                continue

            try:
                videos_resp = yt.videos().list(
                    part="statistics,snippet",
                    id=",".join(video_ids)
                ).execute()
            except Exception as e:
                print("[youtube] videos.list error:", e)
                time.sleep(1)
                continue

            for item in videos_resp.get("items", []):
                stats = item.get("statistics", {})
                snippet = item.get("snippet", {})
                title = snippet.get("title", query)

                views = int(stats.get("viewCount", 0))
                likes = int(stats.get("likeCount", 0)) if stats.get("likeCount") is not None else None
                comments = int(stats.get("commentCount", 0)) if stats.get("commentCount") is not None else None

                out.append({
                    "workflow": title.strip(),
                    "platform": "YouTube",
                    "country": country,
                    "views": views,
                    "likes": likes,
                    "comments": comments,
                    "like_to_view_ratio": safe_ratio(likes, views),
                    "comment_to_view_ratio": safe_ratio(comments, views),
                    "extra": {
                        "videoId": item.get("id"),
                        "channelTitle": snippet.get("channelTitle"),
                        "query": query
                    }
                })

            time.sleep(0.2)

    return out
