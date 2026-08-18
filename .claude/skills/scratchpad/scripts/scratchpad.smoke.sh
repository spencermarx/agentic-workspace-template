#!/usr/bin/env bash
#
# Smoke test for scratchpad.sh — a create → list → clean roundtrip on a disposable
# domain, plus the worktree-rooting guarantees. Self-cleaning; exits non-zero if
# any assertion failed. Not wired into the repo's validate:* chain
# (skill-internal); run it by hand after editing the primitive:
#   bash scratchpad.smoke.sh

set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
sp="$here/scratchpad.sh"
domain="smoke-test"
fails=0

check() { # check <description> <command…> — the command's exit status is the verdict
  local desc="$1"
  shift
  if "$@"; then
    printf 'ok   — %s\n' "$desc"
  else
    printf 'FAIL — %s\n' "$desc"
    fails=$((fails + 1))
  fi
}

# Predicates, so every assertion is a single command `check` can run and report on.
contains() { # contains <text> <substring…> — every substring must appear
  local text="$1" needle
  shift
  # Refuse the two shapes that would assert nothing and still report `ok`: no
  # needles at all (the loop never runs), and an empty needle (`grep -qF ''`
  # matches any input). Both are one shell-quoting slip away in a future caller.
  [ "$#" -gt 0 ] || return 1
  for needle in "$@"; do
    [ -n "$needle" ] || return 1
    printf '%s\n' "$text" | grep -qF "$needle" || return 1
  done
}
starts_with() { case "$1" in "$2"*) ;; *) return 1 ;; esac; }
ends_with() { case "$1" in *"$2") ;; *) return 1 ;; esac; }

# new: creates a directory, prints its path, slugifies the description.
d1="$("$sp" new "$domain" 'Hello, World!')"
check "new creates the directory" test -d "$d1"
check "new slugifies the description" ends_with "$(basename "$d1")" '-hello-world'

# new again: never collides.
d2="$("$sp" new "$domain" 'another one')"
check "new never returns a duplicate path" test "$d1" != "$d2"

# new under concurrency: N racing same-slug callers must each get a distinct dir.
# The sequential checks above pass even with a TOCTOU race; this is the real guard.
race_n=25
race_out="$(mktemp -d)"
for i in $(seq 1 "$race_n"); do ("$sp" new "$domain" 'race' >"$race_out/w$i" 2>/dev/null) & done
wait
race_distinct="$(sort -u "$race_out"/w* 2>/dev/null | grep -c . || true)"
check "new is collision-free under $race_n concurrent same-slug callers" \
  test "$race_distinct" -eq "$race_n"
rm -rf "$race_out"

# list: both entries appear.
listing="$("$sp" list "$domain")"
check "list shows both entries" contains "$listing" "$d1" "$d2"

# clean dry-run: reports, does not delete.
dry="$("$sp" clean "$domain" --older-than 0d)"
check "clean dry-run reports what it would remove" contains "$dry" 'would remove'
check "clean dry-run deletes nothing" test -d "$d1"

# clean --force: actually deletes.
"$sp" clean "$domain" --older-than 0d --force >/dev/null
check "clean --force removes the first entry" test ! -d "$d1"
check "clean --force removes the second entry" test ! -d "$d2"

# ignore guarantee.
root="$("$sp" root)"
root="${root%/.scratchpad}"
check ".scratchpad is git-ignored" git -C "$root" check-ignore -q .scratchpad

# tidy: drop the now-empty smoke-test domain dir if present.
rmdir "$root/.scratchpad/$domain" 2>/dev/null || true

# ---------------------------------------------------------------------------
# Worktree rooting. Every check above runs in the main tree and stays green even
# if the verbs root at the caller's own worktree — which is exactly the bug this
# section exists to catch. The fixtures are disposable repos, so the assertions
# hold no matter how the developer's own checkout happens to be arranged.
# ---------------------------------------------------------------------------

# Resolved with `pwd -P`: on macOS mktemp hands back a /var symlink while git
# reports the /private/var target, and the assertions below compare paths.
tmp="$(cd "$(mktemp -d)" && pwd -P)"
trap 'rm -rf "$tmp"' EXIT
git_q() { git -c user.email=smoke@example.invalid -c user.name=smoke "$@"; }

fixture="$tmp/main"
mkdir -p "$fixture"
git_q -C "$fixture" init -q
printf 'node_modules/\n' >"$fixture/.gitignore" # deliberately WITHOUT .scratchpad/
printf 'x\n' >"$fixture/README.md"
git_q -C "$fixture" add -A
git_q -C "$fixture" commit -qm init
wt="$fixture/.claude/worktrees/wt"
git_q -C "$fixture" worktree add -q --detach "$wt" HEAD

from_main="$(cd "$fixture" && "$sp" new "$domain" 'written from main')"
from_wt="$(cd "$wt" && "$sp" new "$domain" 'written from the worktree')"
check "new from a linked worktree writes to the MAIN root" \
  starts_with "$from_wt" "$fixture/.scratchpad/"

# The payoff: one shared root means either side can find the other's work.
check "list from a worktree sees an entry written from main" \
  contains "$(cd "$wt" && "$sp" list "$domain")" "$from_main"
check "list from main sees an entry written from a worktree" \
  contains "$(cd "$fixture" && "$sp" list "$domain")" "$from_wt"

# A subdirectory is the common case for an agent mid-task; rooting must not move.
mkdir -p "$wt/apps/www"
check "root resolves identically from a nested subdirectory" \
  test "$(cd "$wt/apps/www" && "$sp" root)" = "$fixture/.scratchpad"

# The ignore safety net must never dirty .gitignore — it is a TRACKED file, and
# a dirty one is a commit away from leaking scratch into git.
check "the ignore safety net leaves the tracked .gitignore clean" \
  test -z "$(git -C "$fixture" status --porcelain -- .gitignore)"

# Defense in depth: nothing writes scratch into a worktree any more, but a legacy
# pile left in one must still be unstageable. The directory has to exist for this
# check — `.scratchpad/` is a trailing-slash pattern, so it matches only a path
# git can see IS a directory.
mkdir -p "$wt/.scratchpad"
check "the safety net ignores .scratchpad in every worktree" \
  git -C "$wt" check-ignore -q .scratchpad
rmdir "$wt/.scratchpad"

# Fallback shapes: git names something that is NOT a working tree as the "main
# worktree", and the resolver must notice rather than put scratch outside the
# repo. A bare main repo has no main working tree at all; --separate-git-dir
# makes git report the git dir. Both must fall back to the caller's own tree.
git clone -q --bare "$fixture" "$tmp/bare.git"
git_q -C "$tmp/bare.git" worktree add -q --detach "$tmp/bare-wt" HEAD
check "a bare repo's worktree falls back to its own tree" \
  test "$(cd "$tmp/bare-wt" && "$sp" root)" = "$tmp/bare-wt/.scratchpad"

git_q init -q --separate-git-dir "$tmp/sep-gitdir" "$tmp/sep"
check "--separate-git-dir falls back to the working tree" \
  test "$(cd "$tmp/sep" && "$sp" root)" = "$tmp/sep/.scratchpad"

# No git tree at all. Every verb must REFUSE — the one answer that is never right
# here is a plausible-looking path with a zero exit status, which is how a caller
# ends up creating `/.scratchpad`. `root` failed exactly this way when its
# resolver call sat in argument position, where the guard's `exit` is discarded.
outside="$tmp/not-a-repo"
mkdir -p "$outside"
refuses_outside_repo() { # refuses_outside_repo <verb…>
  # The negation lives INSIDE the subshell so a failed `cd` fails the check rather
  # than inverting into a pass, and the status must be exactly 1 — the guard's
  # refusal. Any-non-zero would accept a usage error (2), reporting `ok` for a
  # typo'd verb that never reached the guard at all.
  (
    cd "$outside" || exit 99
    "$sp" "$@" >/dev/null 2>&1
    [ "$?" -eq 1 ]
  )
}
check "root refuses outside a git repository" refuses_outside_repo root
check "new refuses outside a git repository" refuses_outside_repo new "$domain" 'nope'
check "list refuses outside a git repository" refuses_outside_repo list
check "clean refuses outside a git repository" \
  refuses_outside_repo clean "$domain" --older-than 14d

# The safety net is meant to be dormant wherever the committed .gitignore already
# does the job. The fixture above deliberately OMITS the entry, so it only ever
# exercised the firing path; this one carries it, and must come out untouched.
lacks_line() { # lacks_line <file> <exact-line>
  # The file must EXIST to be judged: `git init` always seeds info/exclude, so an
  # absent one means the path is wrong and the assertion read nothing.
  [ -f "$1" ] && ! grep -qxF "$2" "$1"
}
covered="$tmp/covered"
mkdir -p "$covered"
git_q -C "$covered" init -q
printf '.scratchpad/\n' >"$covered/.gitignore"
printf 'x\n' >"$covered/README.md"
git_q -C "$covered" add -A
git_q -C "$covered" commit -qm init
(cd "$covered" && "$sp" new "$domain" 'first entry in a fresh clone' >/dev/null)
check "the safety net stays dormant when .gitignore already covers .scratchpad" \
  lacks_line "$covered/.git/info/exclude" '.scratchpad/'

echo
if [ "$fails" -eq 0 ]; then
  echo "all checks passed"
else
  echo "$fails check(s) failed"
  exit 1
fi
