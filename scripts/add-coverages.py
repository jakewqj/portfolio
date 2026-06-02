"""
Add new coverage entries to src/data/coverage.json.
Run from portfolio repo root: python scripts/add-coverages.py
"""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COVERAGE_JSON = REPO_ROOT / "src" / "data" / "coverage.json"


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[\s/_]+", "-", text)
    text = re.sub(r"[^a-z0-9\-一-鿿]", "", text)
    return text.strip("-") or "unknown"


# ── New clippings ────────────────────────────────────────────────
new_clippings = [
    # 1
    {"date": "2026-05-08", "year": 2026, "region": "CN", "outlet": "Midifan",
     "outlet_tier": 1, "outlet_category": "instrument-vertical", "outlet_logo": None,
     "campaign_display": "Marketing - HUSH X LIVE", "event": None, "campaign": "hush-x",
     "content_type": "News", "format": "online", "reach": 140000,
     "url": "https://www.midifan.com/modulenews-detailview-59026.htm"},
    # 2
    {"date": "2026-05-08", "year": 2026, "region": "CN", "outlet": "叉烧网",
     "outlet_tier": 2, "outlet_category": "instrument-vertical", "outlet_logo": None,
     "campaign_display": "Marketing - HUSH X LIVE", "event": None, "campaign": "hush-x",
     "content_type": "News", "format": "online", "reach": 60000,
     "url": "https://www.exound.com/articles/23c94e5d-b6eb-4e83-9a6e-78e89a60dbf2"},
    # 3 — print, no URL
    {"date": "2026-06-01", "year": 2026, "region": "CN", "outlet": "《乐器》杂志",
     "outlet_tier": 2, "outlet_category": "instrument-vertical", "outlet_logo": None,
     "campaign_display": "Marketing - HUSH X LIVE", "event": None, "campaign": "hush-x",
     "content_type": "News", "format": "print", "reach": 20000,
     "url": ""},
    # 4
    {"date": "2026-05-09", "year": 2026, "region": "CN", "outlet": "Midifan",
     "outlet_tier": 1, "outlet_category": "instrument-vertical", "outlet_logo": None,
     "campaign_display": "Marketing - HUSH X LIVE", "event": None, "campaign": "hush-x",
     "content_type": "Social", "format": "online", "reach": 140000,
     "url": "https://mp.weixin.qq.com/s/PoF1tIddsqqw82U5xdnhGQ"},
    # 5
    {"date": "2026-05-10", "year": 2026, "region": "CN", "outlet": "搜狐",
     "outlet_tier": 1, "outlet_category": "mass-media", "outlet_logo": None,
     "campaign_display": "Marketing - HUSH X LIVE", "event": None, "campaign": "hush-x",
     "content_type": "News", "format": "online", "reach": 1059,
     "url": "https://www.sohu.com/a/1020621232_121124377"},
    # 6
    {"date": "2026-05-20", "year": 2026, "region": "US", "outlet": "Worship Musician",
     "outlet_tier": 2, "outlet_category": "music-culture", "outlet_logo": None,
     "campaign_display": "Guitar - CV-3", "event": None, "campaign": None,
     "content_type": "Feature", "format": "online", "reach": None,
     "url": "https://viewer.joomag.com/wm-worship-leader-buyers-guide-14-2026/0644304001778896900/p54"},
    # 7
    {"date": "2026-05-20", "year": 2026, "region": "US", "outlet": "Worship Musician",
     "outlet_tier": 2, "outlet_category": "music-culture", "outlet_logo": None,
     "campaign_display": "Effects - Double Swords", "event": None, "campaign": None,
     "content_type": "Round-up", "format": "online", "reach": None,
     "url": "https://viewer.joomag.com/wm-worship-leader-buyers-guide-14-2026/0644304001778896900/p54"},
    # 8
    {"date": "2026-05-20", "year": 2026, "region": "US", "outlet": "Worship Musician",
     "outlet_tier": 2, "outlet_category": "music-culture", "outlet_logo": None,
     "campaign_display": "Guitar - HLX-500", "event": None, "campaign": None,
     "content_type": "Feature", "format": "online", "reach": None,
     "url": "https://viewer.joomag.com/wm-worship-leader-buyers-guide-14-2026/0644304001778896900/p54"},
    # 9
    {"date": "2026-05-10", "year": 2026, "region": "CN", "outlet": "吉他中国-公众号",
     "outlet_tier": 2, "outlet_category": "instrument-vertical", "outlet_logo": None,
     "campaign_display": "Marketing - HUSH X LIVE", "event": None, "campaign": "hush-x",
     "content_type": "News", "format": "online", "reach": 150000,
     "url": ""},
    # 10
    {"date": "2026-05-22", "year": 2026, "region": "US", "outlet": "Music Inc",
     "outlet_tier": 1, "outlet_category": "instrument-vertical", "outlet_logo": None,
     "campaign_display": "Marketing - HUSH X LIVE", "event": None, "campaign": "hush-x",
     "content_type": "News", "format": "online", "reach": 20000,
     "url": "https://www.musicincmag.com/gear/detail/donner-hush-x-live-and-hush-x-live-pro"},
    # 11
    {"date": "2026-05-22", "year": 2026, "region": "US", "outlet": "Mikesgig",
     "outlet_tier": 3, "outlet_category": "instrument-vertical", "outlet_logo": None,
     "campaign_display": "Marketing - HUSH X LIVE", "event": None, "campaign": "hush-x",
     "content_type": "News", "format": "online", "reach": 5000,
     "url": "https://mikesgig.com/guitars-with-built-in-speaker-donner-unveils-hush-x-live-and-hush-x-live-pro-guitars"},
    # 12
    {"date": "2026-05-22", "year": 2026, "region": "US", "outlet": "Guitar World",
     "outlet_tier": 1, "outlet_category": "instrument-vertical", "outlet_logo": None,
     "campaign_display": "Marketing - HUSH X LIVE", "event": None, "campaign": "hush-x",
     "content_type": "Round-up", "format": "online", "reach": 8607000,
     "url": "https://www.guitarworld.com/gear/guitar-gear-round-up-may-23-2026"},
    # 13
    {"date": "2026-05-22", "year": 2026, "region": "US", "outlet": "Guitar World",
     "outlet_tier": 1, "outlet_category": "instrument-vertical", "outlet_logo": None,
     "campaign_display": "Marketing - HUSH X LIVE", "event": None, "campaign": "hush-x",
     "content_type": "News", "format": "online", "reach": 8607000,
     "url": "https://www.guitarworld.com/gear/electric-guitars/donner-hush-x-live-pro-travel-guitar-with-detachable-speaker"},
    # 14
    {"date": "2026-05-22", "year": 2026, "region": "US", "outlet": "Guitar World",
     "outlet_tier": 1, "outlet_category": "instrument-vertical", "outlet_logo": None,
     "campaign_display": "Marketing - HUSH X LIVE", "event": None, "campaign": "hush-x",
     "content_type": "Social", "format": "online", "reach": None,
     "url": "https://www.facebook.com/GuitarWorld/posts/pfbid02Z6pc1ZMZxEFRXmfp4Majk6QXfFXcqhGmzp2t22DUi3hkUoKRAvYwGWjRMZj8jtgUl"},
    # 15
    {"date": "2026-05-22", "year": 2026, "region": "US", "outlet": "MSN",
     "outlet_tier": 1, "outlet_category": "mass-media", "outlet_logo": None,
     "campaign_display": "Marketing - HUSH X LIVE", "event": None, "campaign": "hush-x",
     "content_type": "News", "format": "online", "reach": None,
     "url": "https://www.msn.com/en-us/lifestyle/shopping/donner-just-dropped-the-ultimate-take-anywhere-guitar-a-headless-electric-with-amp-and-speaker/ar-AA23PYVo"},
    # 16
    {"date": "2026-05-16", "year": 2026, "region": "CN", "outlet": "叉烧网",
     "outlet_tier": 2, "outlet_category": "instrument-vertical", "outlet_logo": None,
     "campaign_display": "Event - May Performances", "event": None, "campaign": None,
     "content_type": "News", "format": "online", "reach": None,
     "url": "https://www.exound.com/articles/f75a8482-458b-471b-bfb0-c1d9d8e0f2b7"},
    # 17
    {"date": "2026-05-23", "year": 2026, "region": "US", "outlet": "Yahoo",
     "outlet_tier": 1, "outlet_category": "mass-media", "outlet_logo": None,
     "campaign_display": "Marketing - HUSH X LIVE", "event": None, "campaign": "hush-x",
     "content_type": "News", "format": "online", "reach": 3391000000,
     "url": "https://tech.yahoo.com/audio/articles/welcome-future-people-donner-just-153034948.html"},
    # 18
    {"date": "2026-05-25", "year": 2026, "region": "UK", "outlet": "Guitar Interactive",
     "outlet_tier": 2, "outlet_category": "instrument-vertical", "outlet_logo": None,
     "campaign_display": "Marketing - HUSH X LIVE", "event": None, "campaign": "hush-x",
     "content_type": "News", "format": "online", "reach": None,
     "url": "https://guitarinteractivemagazine.com/news/donner-launches-hush-x-live-guitars-with-detachable-speaker-at-osaka-guitar-show-2026/"},
    # 19
    {"date": "2026-05-28", "year": 2026, "region": "JP", "outlet": "Digimart",
     "outlet_tier": 2, "outlet_category": "instrument-vertical", "outlet_logo": None,
     "campaign_display": "Drum - Beat Pro", "event": None, "campaign": None,
     "content_type": "Social", "format": "online", "reach": 30000,
     "url": "https://x.com/drumsmagazinejp/status/2057296053607784607"},
    # 20
    {"date": "2026-05-25", "year": 2026, "region": "UK", "outlet": "MusicRadar",
     "outlet_tier": 1, "outlet_category": "instrument-vertical", "outlet_logo": None,
     "campaign_display": "Marketing - HUSH X LIVE", "event": None, "campaign": "hush-x",
     "content_type": "News", "format": "online", "reach": 7548000,
     "url": "https://www.musicradar.com/guitars/hush-x-live-pro-travel-guitar-with-onboard-amp-and-detachable-speaker"},
    # 21
    {"date": "2026-05-26", "year": 2026, "region": "US", "outlet": "Yahoo",
     "outlet_tier": 1, "outlet_category": "mass-media", "outlet_logo": None,
     "campaign_display": "Marketing - HUSH X LIVE", "event": None, "campaign": "hush-x",
     "content_type": "News", "format": "online", "reach": 3391000000,
     "url": "https://tech.yahoo.com/audio/articles/donner-reinvents-travel-guitar-headless-130607144.html"},
    # 22
    {"date": "2026-06-02", "year": 2026, "region": "JP", "outlet": "VROCKHK",
     "outlet_tier": 3, "outlet_category": "music-culture", "outlet_logo": None,
     "campaign_display": "Event - Double Swords (Offline)", "event": "Double Swords", "campaign": None,
     "content_type": "News", "format": "online", "reach": 8607000,
     "url": "https://vrockhk.com/2026/06/02/59640/"},
]


def main():
    # Read existing data
    with COVERAGE_JSON.open(encoding="utf-8") as f:
        data = json.load(f)

    existing_clippings = data["clippings"]

    # Build seen_ids from existing to handle dedup
    seen_ids: dict[str, int] = {}
    for c in existing_clippings:
        base = f"{c['date']}-{slugify(c['outlet'])}"
        seen_ids[base] = seen_ids.get(base, 0) + 1

    # Assign IDs to new clippings
    for c in new_clippings:
        base = f"{c['date']}-{slugify(c['outlet'])}"
        count = seen_ids.get(base, 0)
        seen_ids[base] = count + 1
        c["id"] = base if count == 0 else f"{base}-{count + 1}"

    # Merge and sort (newest first)
    all_clippings = existing_clippings + new_clippings
    all_clippings.sort(key=lambda c: (c["date"], c["outlet"]), reverse=True)

    # Recompute totals
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

    COVERAGE_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ Added {len(new_clippings)} new clippings")
    print(f"   Total: {len(all_clippings)} clippings, {unique_outlets} outlets")
    print(f"   Cumulative reach: {total_reach:,}")
    print(f"   By year: {dict(sorted(by_year.items()))}")
    print(f"   By campaign: {dict(by_campaign)}")


if __name__ == "__main__":
    main()
