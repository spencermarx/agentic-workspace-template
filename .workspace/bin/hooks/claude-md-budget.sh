#!/bin/sh
# PostToolUse guard: tell the agent, in the same turn, when it just pushed a
# CLAUDE.md over budget.
#
# Speed is the whole point. A commit hook and CI are backstops; accretion is
# prevented by feedback arriving while the agent still has the edit in mind.
set -eu
set +x  # never trace-expand: tool payloads can carry content that should not land in a transcript

root="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
payload=$(cat 2>/dev/null || true)

# Cheap extraction: we only care whether a CLAUDE.md was touched.
case "$payload" in
  *CLAUDE.md*) ;;
  *) exit 0 ;;
esac

exec python3 - "$root" <<'PY'
import sys, os
sys.path.insert(0, os.path.join(sys.argv[1], ".workspace", "bin"))
try:
    import workspace as ws
except Exception:
    raise SystemExit(0)

budgets = ws.budgets_from(ws.load_config())
paths = ws.claude_md_files()
over = []
for p in paths:
    r = ws.rel(p)
    if r == ".claude/CLAUDE.md":
        continue
    size = len(ws.read_text(p).encode("utf-8"))
    tier = ws.tier_of(p, paths)
    cap = {"root": budgets["rootMaxBytes"],
           "router": budgets["routerMaxBytes"],
           "leaf": budgets["leafMaxBytes"]}[tier]
    if size > cap:
        over.append((r, tier, size, cap))

if over:
    for r, tier, size, cap in over:
        print("%s is %d B, over the %s cap of %d B." % (r, size, tier, cap), file=sys.stderr)
    print("Move the detail into linked docs and add rows to the "
          "'| File | When to load |' table. A leaf CLAUDE.md is a router into "
          "context, not the context.", file=sys.stderr)
    raise SystemExit(2)
PY
