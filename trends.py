#!/usr/bin/env python3
"""Rozana US trending topics dashboard — kisi API key ki zaroorat nahi.

Sources: Google Trends (US) + muft news RSS feeds.
Output: index.html (mobile-friendly dashboard) + data.json
"""
import html
import json
import re
import urllib.parse
from datetime import datetime, timezone

import feedparser

FB_SEARCH = "https://www.facebook.com/search/top/?q="


def fb_link(q):
    return FB_SEARCH + urllib.parse.quote(q)


def google_link(q):
    return "https://www.google.com/search?q=" + urllib.parse.quote(q)


def get_google_trends():
    """Google Trends US — official RSS, kisi key ki zaroorat nahi."""
    items = []
    try:
        f = feedparser.parse(
            "https://trends.google.com/trending/rss?geo=US",
            agent="trending-tool/1.0",
        )
        for e in f.entries[:12]:
            t = re.sub(r"\s+", " ", e.get("title", "")).strip()
            if t:
                items.append({"title": t, "source": "Google Trends US", "kind": "trend"})
    except Exception as e:
        print("google trends rss failed:", e)
    return items


RSS_FEEDS = [
    ("BBC US", "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml"),
    ("NPR", "https://feeds.npr.org/1001/rss.xml"),
    ("Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml"),
]


def get_news():
    items = []
    for name, url in RSS_FEEDS:
        try:
            f = feedparser.parse(url, agent="trending-tool/1.0")
            for e in f.entries[:8]:
                title = re.sub(r"\s+", " ", e.get("title", "")).strip()
                if title:
                    items.append({
                        "title": title,
                        "source": name,
                        "kind": "news",
                        "link": e.get("link", ""),
                    })
        except Exception as e:
            print(name, "rss failed:", e)
    return items


def dedupe(items):
    seen, out = set(), []
    for it in items:
        k = re.sub(r"[^a-z0-9]", "", it["title"].lower())[:60]
        if k and k not in seen:
            seen.add(k)
            out.append(it)
    return out


def card(it):
    t = html.escape(it["title"])
    src = html.escape(it["source"])
    badge = "TREND" if it["kind"] == "trend" else "NEWS"
    bcolor = "#d4af37" if it["kind"] == "trend" else "#4a90d9"
    main_btn = ""
    if it.get("link"):
        main_btn = f'<a class="btn" href="{html.escape(it["link"])}" target="_blank">Khabar kholo</a>'
    else:
        main_btn = f'<a class="btn" href="{google_link(it["title"])}" target="_blank">Google par dekho</a>'
    return f"""
    <div class="card">
      <span class="badge" style="background:{bcolor}">{badge}</span>
      <span class="src">{src}</span>
      <h3>{t}</h3>
      <div class="row">
        <a class="btn fb" href="{fb_link(it["title"])}" target="_blank">Facebook par dekho</a>
        {main_btn}
      </div>
    </div>"""


def build_html(items, generated):
    cards = "\n".join(card(it) for it in items[:24])
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Trending Dashboard</title>
<style>
body{{font-family:system-ui,sans-serif;background:#0a1628;color:#fff;margin:0;padding:16px;max-width:640px;margin:auto}}
h1{{color:#d4af37;font-size:22px}} .sub{{color:#9aa2b2;font-size:13px;margin:-8px 0 12px}}
.howto{{background:#14263f;border:1px solid #d4af37;border-radius:10px;padding:12px;font-size:14px;margin-bottom:14px}}
.card{{background:#14263f;border-radius:12px;padding:14px;margin-bottom:12px}}
.badge{{color:#0a1628;font-size:11px;font-weight:bold;padding:3px 10px;border-radius:20px}}
.src{{color:#9aa2b2;font-size:12px;margin-left:8px}}
h3{{font-size:17px;margin:10px 0 12px;line-height:1.4}}
.row{{display:flex;gap:10px}}
.btn{{flex:1;text-align:center;background:#2a3f5f;color:#fff;text-decoration:none;padding:10px;border-radius:8px;font-size:14px}}
.btn.fb{{background:#1877f2;font-weight:bold}}
</style></head><body>
<h1>Trending Dashboard</h1>
<p class="sub">Updated: {generated} (PKT) — roz subah 9 baje fresh hota hai</p>
<div class="howto">
<b>Kaise use karo:</b><br>
1. Neeche se 1 topic chuno jo tumhare page se match kare<br>
2. <b>Facebook par dekho</b> dabao — wahan ki viral posts dekho<br>
3. Apne alfaaz mein post banao (copy-paste mat karo)
</div>
{cards}
<p class="sub">Sources: Google Trends US, AP, BBC, NPR. Facebook links sirf search kholte hain.</p>
</body></html>"""


def main():
    items = dedupe(get_google_trends() + get_news())
    now = datetime.now(timezone.utc).astimezone()
    stamp = now.strftime("%d %b %Y, %I:%M %p")
    html_out = build_html(items, stamp)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_out)
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"generated": stamp, "items": items}, f, ensure_ascii=False, indent=1)
    print(f"done: {len(items)} topics -> index.html")


if __name__ == "__main__":
    main()
