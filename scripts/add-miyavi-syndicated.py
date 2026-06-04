"""Add 百家号 + 东方财富网 syndicated entries for the 2023 MIYAVI Music China article."""
import json
from collections import Counter
from datetime import datetime

COVERAGE = "d:/jakewqj/portfolio/src/data/coverage.json"

with open(COVERAGE, encoding="utf-8") as f:
    data = json.load(f)

# These 2 were syndicated from 砍柴网's original article
new_clippings = [
    {
        "date": "2023-10-12",
        "year": 2023,
        "region": "CN",
        "outlet": "百家号",
        "outlet_tier": 2,
        "outlet_category": "mass-media",
        "outlet_logo": None,
        "campaign_display": "Event - MIYAVI at Music China 2023",
        "event": "MusicChina 2023",
        "campaign": None,
        "content_type": "News",
        "format": "online",
        "reach": None,
        "url": "https://baijiahao.baidu.com/s?id=1779543503893966213",
    },
    {
        "date": "2023-10-13",
        "year": 2023,
        "region": "CN",
        "outlet": "东方财富网",
        "outlet_tier": 2,
        "outlet_category": "mass-media",
        "outlet_logo": None,
        "campaign_display": "Event - MIYAVI at Music China 2023",
        "event": "MusicChina 2023",
        "campaign": None,
        "content_type": "News",
        "format": "online",
        "reach": None,
        "url": "https://caifuhao.eastmoney.com/news/20231013170345953397560",
    },
]

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

data["generated_at"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"
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

print(f"Added {len(new_clippings)} entries: 百家号 + 东方财富网 (syndicated from 砍柴网)")
print(f"Total: {len(all_clippings)} clippings, {unique_outlets} outlets")
print(f"2023 count: {by_year[2023]}")
