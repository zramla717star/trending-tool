#!/usr/bin/env python3
"""Push trending-tool to GitHub (reuses the github skill, skips .venv)."""
import sys

sys.path.insert(0, "/home/hatch/workspace/skills/github/bin")
import gh_push

gh_push.EXCLUDE_DIRS = gh_push.EXCLUDE_DIRS | {".venv"}
sys.argv = ["gh_push.py", "--root", "~/workspace/trending-tool", "--repo", "trending-tool"]
gh_push.main()
