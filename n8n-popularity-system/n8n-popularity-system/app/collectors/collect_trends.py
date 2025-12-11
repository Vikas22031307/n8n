from typing import List, Dict
from pytrends.request import TrendReq
from ..config import TREND_KEYWORDS, COUNTRIES
import time

def collect_trends_workflows() -> List[Dict]:
    py = TrendReq(hl="en-US", tz=0)
    out = []

    for country in COUNTRIES:
        geo = "US" if country == "US" else "IN"
        try:
            py.build_payload(TREND_KEYWORDS, timeframe="today 3-m", geo=geo)
            df = py.interest_over_time()
        except Exception as e:
            print("[trends] error:", e)
            time.sleep(1)
            continue

        if df.empty:
            continue

        for kw in TREND_KEYWORDS:
            series = df.get(kw)
            if series is None:
                continue
            series = series.dropna()
            if series.empty:
                continue

            last = series.tail(30).mean()
            first = series.head(30).mean()
            change = None
            if first and first != 0:
                change = ((last - first) / first) * 100.0

            monthly_volume = int(last * 100)

            out.append({
                "workflow": kw,
                "platform": "Google",
                "country": country,
                "monthly_search_volume": monthly_volume,
                "change_last_60_days": change,
                "extra": {"source": "pytrends", "keyword": kw}
            })

        time.sleep(0.5)

    return out
