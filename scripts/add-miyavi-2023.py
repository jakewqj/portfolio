"""Add 2023 Music China MIYAVI search-discovered entries to coverage.json."""
import json
from collections import Counter
from datetime import datetime

COVERAGE = "d:/jakewqj/portfolio/src/data/coverage.json"

with open(COVERAGE, encoding="utf-8") as f:
    data = json.load(f)

new_clippings = [
    {
        "date": "2023-10-12", "year": 2023, "region": "CN",
        "outlet": "科技快报", "outlet_tier": 3, "outlet_category": "mass-media", "outlet_logo": None,
        "campaign_display": "Event - MIYAVI at Music China 2023", "event": "MusicChina 2023", "campaign": None,
        "content_type": "News", "format": "online", "reach": None,
        "url": "http://news.ikanchai.com/2023/1012/562719.shtml"
    },
    {
        "date": "2024-10-17", "year": 2024, "region": "CN",
        "outlet": "中国企业报", "outlet_tier": 3, "outlet_category": "mass-media", "outlet_logo": None,
        "campaign_display": "Effects - Double Swords", "event": None, "campaign": None,
        "content_type": "News", "format": "online", "reach": 4421,
        "url": "https://www.zqbao.com.cn/news/1184.html"
    },
]

# Build seen_ids
existing = data["clippings"]
seen_ids = {}
for c in existing:
    base = f"{c['date']}-{c['outlet'].lower().strip()}"
    seen_ids[base] = seen_ids.get(base, 0) + 1

for c in new_clippings:
    base = f"{c['date']}-{c['outlet'].lower().strip()}"
    count = seen_ids.get(base, 0)
    seen_ids[base] = count + 1
    c["id"] = base if count == 0 else f"{base}-{count + 1}"

all_clippings = existing + new_clippings
all_clippings.sort(key=lambda c: (c["date"], c["outlet"]), reverse=True)

total_reach = sum((c["reach"] or 0) for c in all_clippings)
unique_outlets = len({c["outlet"] for c in all_clippings})
regions = sorted({c["region"] for c in all_clippings if c["region"]})
by_year = Counter(c["year"] for c in all_clippings)
by_campaign = Counter(c["campaign"] for c in all_clippings if c["campaign"])

data["generated_at"] = datetime.now(datetime.UTC).isoformat(timespec="seconds") + "Z" if hasattr(datetime, "UTC") else datetime.utcnow().isoformat(timespec="seconds") + "Z"
data["totals"] = {
    "clippings": len(all_clippings),
    "outlets": unique_outlets,
    "regions": regions,
    "cumulative_reach": total_reach,
    "by_year": dict(sorted(by_year.items())),
    "by_campaign": dict(by_campaign),
}
data["clippings"] = all_clippings

with open(COVERAGE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Added {len(new_clippings)} entries. Total: {len(all_clippings)} clippings, {unique_outlets} outlets")
print(f"Cumulative reach: {total_reach:,}")
print(f"By year: {dict(sorted(by_year.items()))}")
print(f"By campaign: {dict(by_campaign)}")
