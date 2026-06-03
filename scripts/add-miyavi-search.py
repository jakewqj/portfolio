"""Add 5 search-discovered MIYAVI entries to coverage.json."""
import json, re
from collections import Counter
from datetime import datetime

def slugify(text):
    text = text.strip().lower()
    text = re.sub(r"[\s/_]+", "-", text)
    text = re.sub(r"[^a-z0-9\-一-鿿]", "", text)
    return text.strip("-") or "unknown"

COVERAGE = "d:/jakewqj/portfolio/src/data/coverage.json"

with open(COVERAGE, encoding="utf-8") as f:
    data = json.load(f)

new_clippings = [
    {
        "date": "2025-10-28", "year": 2025, "region": "US",
        "outlet": "Guitar World", "outlet_tier": 1, "outlet_category": "instrument-vertical", "outlet_logo": None,
        "campaign_display": "Effects - Double Swords", "event": None, "campaign": None,
        "content_type": "Feature", "format": "online", "reach": 8607000,
        "url": "https://www.guitarworld.com/gear/guitar-pedals/donner-x-miyavi-double-swords-pedals"
    },
    {
        "date": "2023-10-12", "year": 2023, "region": "CN",
        "outlet": "电子工程专辑", "outlet_tier": 3, "outlet_category": "mass-media", "outlet_logo": None,
        "campaign_display": "Event - MIYAVI at Music China 2023", "event": "MusicChina 2023", "campaign": None,
        "content_type": "News", "format": "online", "reach": None,
        "url": "https://www.eet-china.com/mp/a257755.html"
    },
    {
        "date": "2024-10-16", "year": 2024, "region": "CN",
        "outlet": "美通社", "outlet_tier": 3, "outlet_category": "newswire", "outlet_logo": None,
        "campaign_display": "Effects - Double Swords", "event": None, "campaign": None,
        "content_type": "News", "format": "online", "reach": None,
        "url": "https://www.prnasia.com/story/464655-1.shtml"
    },
    {
        "date": "2025-10-24", "year": 2025, "region": "CN",
        "outlet": "什么值得买", "outlet_tier": 3, "outlet_category": "mass-media", "outlet_logo": None,
        "campaign_display": "Effects - Double Swords", "event": None, "campaign": None,
        "content_type": "Review", "format": "online", "reach": None,
        "url": "https://post.smzdm.com/zz/p/ax647x32/"
    },
    {
        "date": "2024-10-01", "year": 2024, "region": "CN",
        "outlet": "知乎", "outlet_tier": 2, "outlet_category": "mass-media", "outlet_logo": None,
        "campaign_display": "Event - MIYAVI Creative Director Announcement", "event": "MusicChina 2024", "campaign": None,
        "content_type": "News", "format": "online", "reach": None,
        "url": "https://zhuanlan.zhihu.com/p/660236502"
    },
]

existing = data["clippings"]
seen_ids = {}
for c in existing:
    base = f"{c['date']}-{slugify(c['outlet'])}"
    seen_ids[base] = seen_ids.get(base, 0) + 1

for c in new_clippings:
    base = f"{c['date']}-{slugify(c['outlet'])}"
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

print(f"Added {len(new_clippings)} entries. Total: {len(all_clippings)} clippings, {unique_outlets} outlets")
print(f"Cumulative reach: {total_reach:,}")
print(f"By year: {dict(sorted(by_year.items()))}")
