#!/usr/bin/env python3
"""data.json se rozana ka chhota Roman Urdu trends message banao (chat ke liye).

Usage: python3 trends_chat.py  -> stdout par message
data.json roz subah trending-dashboard-daily cron se fresh hota hai (9:06 PKT).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data.json")


def clean(t, n=60):
    t = re.sub(r"\s+", " ", t or "").strip()
    return t if len(t) <= n else t[: n - 1] + "…"


def main():
    try:
        d = json.load(open(DATA, encoding="utf-8"))
    except Exception as e:
        print("data.json nahi mila:", e)
        sys.exit(1)
    items = d.get("items", [])
    gen = d.get("generated", "")

    gt = [clean(i["title"], 45) for i in items
          if i["source"] == "Google Trends US"][:6]
    yt = [clean(i["title"], 50) for i in items
          if i["source"] == "YouTube Trending US"][:3]
    nw = [clean(i["title"], 60) for i in items if i["kind"] == "news"][:3]

    lines = []
    lines.append("Aaj ke US trends " + (f"({gen})" if gen else "") + ":")
    if gt:
        lines.append("")
        lines.append("🔥 Google US: " + ", ".join(gt))
    if yt:
        lines.append("")
        lines.append("🎬 YouTube: " + ", ".join(yt))
    if nw:
        lines.append("")
        lines.append("📰 News:")
        for n in nw:
            lines.append("• " + n)
    lines.append("")
    lines.append("Map video ka idea chahiye to bolo — in mein se chun kar bata dungi.")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
