#!/usr/bin/env python3
"""The workspace engine: structure generation and the validation gate.

Python 3.9 compatible, standard library only. `/usr/bin/python3` ships with the
Xcode Command Line Tools, the same package that provides git, so anyone who can
clone this repo can run this file. That is the whole reason it is not Node: node
is commonly version-manager-managed and absent from a non-login shell, and a
package.json in an Obsidian vault invites an npm install that drops node_modules
into a folder Obsidian indexes and a sync plugin mirrors.

Structure of this file mirrors the design: pure functions over in-memory sources,
with all I/O confined to the loaders and the CLI tail.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

CONFIG_PATH = REPO_ROOT / ".workspace" / "workspace.json"
PLAN_PATH = REPO_ROOT / ".workspace" / "plan.json"
REGISTRY_PATH = REPO_ROOT / "Standards" / "README.md"

# The three placeholder grammars. All are gated once bootstrapped is true.
#
# The UPPER-first anchor is deliberate and matters more here than in a code repo:
# Obsidian's own Templates plugin uses lowercase {{title}}, {{date:YYYY-MM-DD}},
# {{time}}. Anchoring on an uppercase first character excludes that grammar by
# construction, along with JSX object expressions and Go/Hugo template syntax.
TOKEN_RE = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}")
SENTINEL = "__REPLACE_ME__"
AGENT_COMMENT_RE = re.compile(r"<!--\s*AGENT:")

# A file carrying this in its first 20 lines excludes itself from the mutate
# surface. This replaces bizkit's hand-maintained ignore list: the two skills
# that document the grammars using literal examples opt themselves out, locally
# and un-forgettably, instead of appearing in a registry somewhere else.
NO_MUTATE_MARKER = "<!-- workspace:no-mutate -->"

# Read by code, not just by humans. A skill directory whose SKILL.md carries the
# verbatim marker is excluded whole from the mutate surface, so upstream docs
# containing double-braced UPPER_SNAKE template syntax are never mistaken for
# unreplaced identity. Marker-driven so every future vendoring is covered by the
# provenance line the ADR already requires.
VENDORED_VERBATIM_MARKER = "Vendored verbatim from"
VENDORED_ANY_RE = re.compile(r"Vendored (?:verbatim )?from\s+(\S+)")
VENDORED_SHA_RE = re.compile(r"@\s*([0-9a-f]{7,40})\b")

MUTATE_EXTENSIONS = {
    ".md", ".json", ".yaml", ".yml", ".canvas", ".css",
    ".sh", ".py", ".txt", ".example", ".base",
}

MUTATE_IGNORE_DIRS = {".git", "node_modules", ".trash", "__pycache__", ".scratchpad"}

# Each of these has a reason that must survive, because each is a bug someone
# will otherwise re-introduce.
MUTATE_IGNORE_PATHS = {
    # Vendored plugin builds: minified main.js, never ours to rewrite.
    ".obsidian/plugins",
    # Per-machine UI state, rewritten every session.
    ".obsidian/workspace.json",
    # A template is an inert artifact copied into every FUTURE note. Substituting
    # identity into it bakes a stale name into notes created years from now.
    # Templates reference identity by link, never by baked string.
    "Obsidian/Templates",
    # Binaries and pasted images.
    "Attachments",
    # The scaffold's whole point is that README.md and *.example carry the
    # sentinel FOREVER, until a human pastes a real key. A permanent sentinel
    # here is the design working, not rot.
    ".credentials",
    # The harness itself: engine, templates (which must contain tokens and
    # sentinels), schema, fixtures, and the ADRs documenting the grammar.
    # Excluding one directory replaces six hand-maintained list entries.
    ".workspace",
}

# Per-tier CLAUDE.md byte budgets. Nesting is the point of this architecture; the
# 35KB failure mode in both source repos came from standards and reference
# material living inside CLAUDE.md, not from nesting. The rules layer gives that
# material a cheaper home, and these caps keep it there.
DEFAULT_BUDGETS = {
    "rootMaxBytes": 8000,
    "rootWarnBytes": 5000,
    "routerMaxBytes": 3500,
    "leafMaxBytes": 20000,
    "leafWarnBytes": 14000,
    "ruleMaxBytes": 1200,
    "skillBodyWarnBytes": 5000,
    "skillBodyMaxBytes": 8000,
    "descriptionMaxChars": 500,
    "descriptionsTotalMaxBytes": 14000,
}

# The one rule that fires on every markdown read. It is capped harder than the
# rest and must never grow: if house voice needs more surface it splits into
# narrower globs. This is the single place the mechanism built to solve the
# always-on budget problem could recreate it.
UNIVERSAL_RULE = ".claude/rules/writing/house-voice.md"
UNIVERSAL_RULE_MAX_BYTES = 400

REQUIRED_ROOT_SECTIONS = [
    "## What this workspace is",
    "## Where things live",
    "## Always-on invariants",
    "## What's pending",
]

REQUIRED_LEAF_SECTIONS = [
    "## TL;DR for picking up cold",
    "## Where context lives",
    "## Working norms",
    "## Open questions",
    "## Recent activity",
    "## What's pending",
]

# Standards arrive via path globs. A "## Standards" heading in any CLAUDE.md means
# someone is paying the always-on price for something conditional.
PROHIBITED_CLAUDE_SECTION = "## Standards"

# Identity that must never survive into a published template. Paths under these
# prefixes are exempt because provenance, licensing, and stub-wiring notes
# legitimately name their origin.
IDENTITY_TERMS = ["spencermarx", "aclarify", "bizkit", "wrkbelt", "donostia"]
IDENTITY_EXEMPT_PREFIXES = (
    "Decisions/", "LICENSE", "THIRD-PARTY-NOTICES.md",
    ".claude/skills/_stubs/", ".workspace/docs/", "README.md",
)

# Files a template repo is allowed to ship outside the harness directories.
# Anything else is workspace content that must not reach a public repo.
TEMPLATE_CONTENT_WHITELIST = {
    "CLAUDE.md", "CONTEXT.md", "Home.md", "README.md", "THIRD-PARTY-NOTICES.md",
}
TEMPLATE_CONTENT_WHITELIST_DIRS = (
    "Standards/", "Decisions/", "Obsidian/", "instructions/", ".claude/",
    ".workspace/", ".credentials/",
)


# --------------------------------------------------------------------------
# Findings
# --------------------------------------------------------------------------

FAIL = "FAIL"
WARN = "WARN"


@dataclass
class Finding:
    level: str
    code: str
    path: str
    message: str
    hint: str = ""


@dataclass
class Report:
    findings: List[Finding] = field(default_factory=list)

    def fail(self, code: str, path: str, message: str, hint: str = "") -> None:
        self.findings.append(Finding(FAIL, code, path, message, hint))

    def warn(self, code: str, path: str, message: str, hint: str = "") -> None:
        self.findings.append(Finding(WARN, code, path, message, hint))

    @property
    def failures(self) -> List[Finding]:
        return [f for f in self.findings if f.level == FAIL]

    @property
    def warnings(self) -> List[Finding]:
        return [f for f in self.findings if f.level == WARN]


# --------------------------------------------------------------------------
# Minimal YAML frontmatter
# --------------------------------------------------------------------------

def parse_frontmatter(text: str) -> Tuple[Optional[Dict[str, object]], List[str]]:
    """Parse a leading YAML frontmatter block.

    Deliberately supports only the subset this repo's conventions allow: scalar
    values, block sequences, and inline flow arrays. Anything richer is a signal
    the note has outgrown the frontmatter contract, not a parser gap to fill.

    Returns (mapping, key_order). Mapping is None when there is no frontmatter.
    """
    if not text.startswith("---"):
        return None, []
    lines = text.split("\n")
    if lines[0].strip() != "---":
        return None, []
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, []

    data: Dict[str, object] = {}
    order: List[str] = []
    current_key: Optional[str] = None
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith((" ", "\t")) and raw.lstrip().startswith("- "):
            if current_key is not None:
                item = raw.lstrip()[2:].strip().strip("'\"")
                bucket = data.get(current_key)
                if isinstance(bucket, list):
                    bucket.append(item)
                else:
                    data[current_key] = [item]
            continue
        if raw.lstrip().startswith("- ") and current_key is not None:
            item = raw.lstrip()[2:].strip().strip("'\"")
            bucket = data.get(current_key)
            if isinstance(bucket, list):
                bucket.append(item)
            else:
                data[current_key] = [item]
            continue
        if ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        key = key.strip()
        value = value.strip()
        if key not in data:
            order.append(key)
        current_key = key
        if not value:
            data[key] = []
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [p.strip().strip("'\"") for p in inner.split(",") if p.strip()] if inner else []
        elif value.startswith(">-") or value == ">":
            data[key] = ""  # folded scalar; body captured on following lines
        else:
            data[key] = value.strip("'\"")
    return data, order


def frontmatter_body_offset(text: str) -> int:
    """Byte offset where the body begins, so budgets exclude frontmatter."""
    if not text.startswith("---"):
        return 0
    idx = text.find("\n---", 3)
    return 0 if idx == -1 else idx + 4


# --------------------------------------------------------------------------
# Glob matching
# --------------------------------------------------------------------------

# We support **, *, ?, and [abc] only. No braces, no negation, no extglob.
# Restricting the syntax is what lets a small matcher be provably correct, and
# the restriction is stated in Standards/harness-standards.md and enforced below.
SUPPORTED_GLOB_RE = re.compile(r"^[A-Za-z0-9_./*?\[\]{}!,\- ]*$")
UNSUPPORTED_GLOB_TOKENS = ("{", "}", "!", "+(", "@(")


def glob_to_regex(pattern: str) -> re.Pattern:
    out = ["^"]
    i = 0
    n = len(pattern)
    while i < n:
        c = pattern[i]
        if pattern.startswith("**/", i):
            # Zero or more leading path segments.
            out.append("(?:[^/]+/)*")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif c == "*":
            out.append("[^/]*")
            i += 1
        elif c == "?":
            out.append("[^/]")
            i += 1
        elif c == "[":
            j = pattern.find("]", i)
            if j == -1:
                out.append(re.escape(c))
                i += 1
            else:
                out.append("[" + pattern[i + 1:j] + "]")
                i = j + 1
        else:
            out.append(re.escape(c))
            i += 1
    out.append("$")
    return re.compile("".join(out))


def glob_is_supported(pattern: str) -> bool:
    if any(tok in pattern for tok in UNSUPPORTED_GLOB_TOKENS):
        return False
    return bool(SUPPORTED_GLOB_RE.match(pattern))


# --------------------------------------------------------------------------
# Markdown helpers
# --------------------------------------------------------------------------

MD_LINK_RE = re.compile(r"\[(?P<label>[^\]]*)\]\((?P<target>[^)\s]+)\)")
MD_ANGLE_LINK_RE = re.compile(r"\[(?P<label>[^\]]*)\]\(<(?P<target>[^>]+)>\)")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$", re.MULTILINE)
FENCE_RE = re.compile(r"^(?:```|~~~)", re.MULTILINE)


def strip_code_fences(text: str) -> str:
    """Remove fenced blocks entirely and blank out inline code spans.

    Inline spans matter as much as fences here: documentation legitimately shows
    example links and example globs in backticks, and treating those as real
    references produces exactly the kind of false failure that teaches people to
    ignore the gate.
    """
    out = []
    in_fence = False
    for line in text.split("\n"):
        if line.lstrip().startswith("```") or line.lstrip().startswith("~~~"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(re.sub(r"`[^`]*`", "", line))
    return "\n".join(out)


def slugify_heading(text: str) -> str:
    """Reimplementation of GitHub's heading-anchor slugify.

    Anchors are the fragile half of a rules pointer: a renamed heading silently
    stops routing, and nothing reports at read time that a rule failed to load.
    """
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = MD_ANGLE_LINK_RE.sub(r"\g<label>", text)
    text = MD_LINK_RE.sub(r"\g<label>", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return text.replace(" ", "-")


def headings_of(text: str) -> List[Tuple[int, str]]:
    return [(len(m.group(1)), m.group(2).strip()) for m in HEADING_RE.finditer(text)]


def anchors_of(text: str) -> Set[str]:
    return {slugify_heading(h) for _, h in headings_of(text)}


def links_of(text: str) -> List[Tuple[str, str]]:
    """(label, target) for every markdown link outside code fences."""
    body = strip_code_fences(text)
    found = [(m.group("label"), m.group("target")) for m in MD_ANGLE_LINK_RE.finditer(body)]
    consumed = MD_ANGLE_LINK_RE.sub("", body)
    found += [(m.group("label"), m.group("target")) for m in MD_LINK_RE.finditer(consumed)]
    return found


# --------------------------------------------------------------------------
# Loaders
# --------------------------------------------------------------------------

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return ""


def load_config() -> Dict[str, object]:
    if not CONFIG_PATH.exists():
        return {"bootstrapped": False}
    try:
        return json.loads(read_text(CONFIG_PATH))
    except json.JSONDecodeError:
        return {"bootstrapped": False}


def budgets_from(config: Dict[str, object]) -> Dict[str, int]:
    merged = dict(DEFAULT_BUDGETS)
    override = config.get("budgets")
    if isinstance(override, dict):
        for k, v in override.items():
            if isinstance(v, int):
                merged[k] = v
    return merged


def all_repo_files() -> List[Path]:
    out: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in MUTATE_IGNORE_DIRS]
        for name in filenames:
            if name == ".DS_Store":
                continue
            out.append(Path(dirpath) / name)
    return out


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def is_vendored_verbatim_dir(directory: Path) -> bool:
    skill_md = directory / "SKILL.md"
    return skill_md.exists() and VENDORED_VERBATIM_MARKER in read_text(skill_md)


def walk_mutate_surface() -> List[Path]:
    """The single source of truth shared by the writer and the gate.

    Keeping the walk and its exclusions in one function guarantees the gate's
    scan surface can never be narrower than what bootstrap touched.
    """
    vendored_roots: List[str] = []
    skills_dir = REPO_ROOT / ".claude" / "skills"
    if skills_dir.is_dir():
        for child in sorted(skills_dir.iterdir()):
            if child.is_dir() and is_vendored_verbatim_dir(child):
                vendored_roots.append(rel(child) + "/")

    out: List[Path] = []
    for path in all_repo_files():
        relative = rel(path)
        if path.suffix not in MUTATE_EXTENSIONS:
            continue
        if any(relative == p or relative.startswith(p + "/") for p in MUTATE_IGNORE_PATHS):
            continue
        if any(relative.startswith(v) for v in vendored_roots):
            continue
        head = "\n".join(read_text(path).split("\n")[:20])
        if NO_MUTATE_MARKER in head:
            continue
        out.append(path)
    return out


# --------------------------------------------------------------------------
# Checks: rules layer
# --------------------------------------------------------------------------

def rule_files() -> List[Path]:
    rules_dir = REPO_ROOT / ".claude" / "rules"
    if not rules_dir.is_dir():
        return []
    return sorted(p for p in rules_dir.rglob("*.md") if p.is_file())


def check_rules(report: Report, budgets: Dict[str, int], template_mode: bool) -> None:
    content_files = [p for p in all_repo_files() if p.suffix in MUTATE_EXTENSIONS]
    content_rels = [rel(p) for p in content_files]

    for path in rule_files():
        r = rel(path)
        text = read_text(path)
        size = len(text.encode("utf-8"))

        cap = UNIVERSAL_RULE_MAX_BYTES if r == UNIVERSAL_RULE else budgets["ruleMaxBytes"]
        if size > cap:
            hint = ("House voice fires on every markdown read. If it needs more surface it "
                    "splits into narrower globs; it never grows.") if r == UNIVERSAL_RULE else \
                   "A rule is a pointer. Move the substance into its Standards section."
            report.fail("rule-size", r, "%d B exceeds the %d B cap" % (size, cap), hint)

        fm, order = parse_frontmatter(text)
        if fm is None:
            report.fail("rule-frontmatter", r, "no frontmatter",
                        "A rule needs exactly two keys: description, paths.")
            continue
        if order != ["description", "paths"]:
            report.fail(
                "rule-frontmatter", r,
                "frontmatter keys are %s, expected exactly ['description', 'paths']" % order,
                "Two keys, in that order. A third key means the rule is doing more than routing.")

        paths = fm.get("paths")
        if not isinstance(paths, list) or not paths:
            report.fail("rule-paths", r, "paths is empty or not a list")
            continue

        for pattern in paths:
            if not glob_is_supported(pattern):
                report.fail("rule-glob-syntax", r, "unsupported glob syntax: %s" % pattern,
                            "Supported: ** * ? [abc]. No braces, no negation, no extglob.")
                continue
            rx = glob_to_regex(pattern)
            matched = any(rx.match(c) for c in content_rels)
            if not matched:
                # The positive control. This is what proves a folder rename
                # rewrote its globs; without it a rule silently stops routing
                # and the system reads as healthy.
                msg = "glob matches no file in the repo: %s" % pattern
                hint = "Either the folder was renamed without rewriting this glob, or the rule is dead."
                if template_mode:
                    report.warn("rule-glob-dead", r, msg,
                                "Expected before bootstrap: most target folders do not exist yet.")
                else:
                    report.fail("rule-glob-dead", r, msg, hint)

        body = text[frontmatter_body_offset(text):]
        for label, target in links_of(body):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            target_path, _, anchor = target.partition("#")
            resolved = (path.parent / target_path).resolve() if target_path else path
            if not resolved.exists():
                report.fail("rule-link-dead", r, "link target does not resolve: %s" % target)
                continue
            if anchor:
                target_text = read_text(resolved)
                if anchor not in anchors_of(target_text):
                    report.fail("rule-anchor-dead", r,
                                "anchor #%s does not exist in %s" % (anchor, target_path),
                                "A renamed heading stops routing silently. Fix the pointer or the heading.")
                else:
                    # The link LABEL must name the same section as the target
                    # heading. A pointer aimed at a live but wrong section is
                    # the one drift the link check alone cannot catch.
                    label_tail = label.split("§")[-1].strip() if "§" in label else ""
                    if label_tail and slugify_heading(label_tail) != anchor:
                        report.warn("rule-label-mismatch", r,
                                    "link label names '%s' but the anchor is '#%s'" % (label_tail, anchor))

        for line in body.split("\n"):
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "[", "-", ">", "|")) or "](" in line:
                continue
            if re.search(r"\b(must|never|always|do not|don't)\b", stripped, re.IGNORECASE):
                report.warn("rule-restates", r,
                            "imperative outside a link line: %s" % stripped[:70],
                            "A rule that states the rule has stopped being a pointer.")
                break


def check_registry(report: Report) -> None:
    if not REGISTRY_PATH.exists():
        report.fail("registry-missing", rel(REGISTRY_PATH), "the standards registry does not exist")
        return
    registry = read_text(REGISTRY_PATH)
    on_disk = {rel(p) for p in rule_files()}
    # Table rows only. The prose above the table names the shape of a rule path
    # (.claude/rules/<domain>/<slug>.md) and must not be read as a row.
    table_lines = [ln for ln in registry.split("\n") if ln.lstrip().startswith("|")]
    listed = set(re.findall(r"`(\.claude/rules/[^`<>]+\.md)`", "\n".join(table_lines)))

    for missing in sorted(on_disk - listed):
        report.fail("registry-missing-row", rel(REGISTRY_PATH),
                    "rule on disk has no registry row: %s" % missing,
                    "The registry is the drift oracle. Every rule gets a row.")
    for orphan in sorted(listed - on_disk):
        report.fail("registry-orphan-row", rel(REGISTRY_PATH),
                    "registry row points at a rule that does not exist: %s" % orphan)


# --------------------------------------------------------------------------
# Checks: skills
# --------------------------------------------------------------------------

def skill_dirs() -> List[Path]:
    skills = REPO_ROOT / ".claude" / "skills"
    if not skills.is_dir():
        return []
    return sorted(d for d in skills.iterdir() if d.is_dir() and d.name != "_stubs")


def check_skills(report: Report, budgets: Dict[str, int]) -> None:
    skills_root = REPO_ROOT / ".claude" / "skills"
    if not skills_root.is_dir():
        return

    # Only .claude/skills/<name>/SKILL.md may exist. A nested SKILL.md risks
    # auto-registration into the always-resident description budget, which is
    # why both source repos' sub-skill layouts had to be reconciled to one.
    for path in skills_root.rglob("SKILL.md"):
        depth = len(path.relative_to(skills_root).parts)
        if depth != 2:
            report.fail("skill-nested", rel(path),
                        "SKILL.md must be exactly .claude/skills/<name>/SKILL.md",
                        "Sub-skills are flat files: sub-skills/<name>.md, never a nested directory.")

    stubs = skills_root / "_stubs"
    if stubs.is_dir():
        for path in stubs.rglob("*"):
            if path.is_file() and path.name == "SKILL.md":
                report.fail("stub-registrable", rel(path),
                            "a stub named SKILL.md would register and cost context",
                            "Stubs are flat _stubs/<name>.md files.")

    known_skills = {d.name for d in skill_dirs()}
    known_stubs = set()
    if stubs.is_dir():
        known_stubs = {p.stem for p in stubs.glob("*.md") if p.name != "README.md"}

    total_description_bytes = 0
    for directory in skill_dirs():
        skill_md = directory / "SKILL.md"
        r = rel(skill_md)
        if not skill_md.exists():
            report.fail("skill-missing", rel(directory), "skill directory has no SKILL.md")
            continue
        text = read_text(skill_md)
        fm, _ = parse_frontmatter(text)
        if fm is None:
            report.fail("skill-frontmatter", r, "no frontmatter")
            continue

        name = fm.get("name")
        if name and name != directory.name:
            report.fail("skill-name", r, "name '%s' does not match directory '%s'" % (name, directory.name))

        description = fm.get("description")
        if not description or not isinstance(description, str):
            # Folded scalars land here; recover the description from the raw block.
            block = text.split("---")[1] if text.count("---") >= 2 else ""
            m = re.search(r"description:\s*>-?\s*\n((?:\s{2,}.*\n)+)", block)
            description = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
        if not description:
            report.fail("skill-description", r, "description is empty",
                        "The description is the invocation trigger and the whole dispatch mechanism.")
            continue
        if len(description) > budgets["descriptionMaxChars"]:
            report.fail("skill-description-size", r,
                        "description is %d chars, cap %d" % (len(description), budgets["descriptionMaxChars"]))
        total_description_bytes += len(description.encode("utf-8"))

        body = text[frontmatter_body_offset(text):]
        body_bytes = len(body.encode("utf-8"))
        if body_bytes > budgets["skillBodyMaxBytes"]:
            report.fail("skill-body-size", r,
                        "body is %d B, cap %d" % (body_bytes, budgets["skillBodyMaxBytes"]),
                        "Move depth into sub-skills/ or references/, which load on demand.")
        elif body_bytes > budgets["skillBodyWarnBytes"]:
            report.warn("skill-body-size", r,
                        "body is %d B, soft target %d" % (body_bytes, budgets["skillBodyWarnBytes"]))

        if "Vendored" in text:
            m = VENDORED_ANY_RE.search(text)
            if not m:
                report.fail("vendor-marker", r,
                            "mentions vendoring but carries neither provenance marker",
                            "Use: 'Vendored verbatim from <url> (<path> @ <sha>)' or "
                            "'Vendored from <url> (<path>); adapted for this repo (<deltas>)'.")
            elif not VENDORED_SHA_RE.search(text):
                report.fail("vendor-sha", r,
                            "provenance line has no '@ <sha>' pin",
                            "Without a pin there is no way to diff against upstream. "
                            "This is the gap the source repo left open.")

    if total_description_bytes > budgets["descriptionsTotalMaxBytes"]:
        report.fail("descriptions-budget", ".claude/skills",
                    "descriptions total %d B, cap %d" % (total_description_bytes,
                                                         budgets["descriptionsTotalMaxBytes"]),
                    "Every description is resident on every request. Tighten or stub skills.")

    # Skill dependencies are declared as links, so dependency checking is link
    # checking. A backticked skill name that is not also a link is the phrasing
    # that produced seven dangling references in the source workspace.
    for directory in skill_dirs():
        for path in list(directory.rglob("*.md")):
            text = read_text(path)
            body = strip_code_fences(text)
            for match in re.finditer(r"`([a-z0-9][a-z0-9-]{2,})`\s+skill", body):
                referenced = match.group(1)
                if referenced in known_skills or referenced in known_stubs:
                    continue
                report.fail("skill-dep-dangling", rel(path),
                            "references a `%s` skill that does not exist" % referenced,
                            "Either create it, stub it, or drop the reference.")


# --------------------------------------------------------------------------
# Checks: CLAUDE.md tiers
# --------------------------------------------------------------------------

def claude_md_files() -> List[Path]:
    return sorted(p for p in REPO_ROOT.rglob("CLAUDE.md")
                  if p.is_file() and not any(part in MUTATE_IGNORE_DIRS for part in p.parts))


def tier_of(path: Path, all_paths: Sequence[Path]) -> str:
    """Root, router, or leaf.

    A folder whose subtree contains another CLAUDE.md is a router: its only job
    is to point down. Everything else that carries one is a leaf.
    """
    if path.parent == REPO_ROOT:
        return "root"
    here = path.parent
    for other in all_paths:
        if other == path:
            continue
        try:
            other.parent.relative_to(here)
        except ValueError:
            continue
        if other.parent != here:
            return "router"
    return "leaf"


def check_claude_md(report: Report, budgets: Dict[str, int], template_mode: bool) -> None:
    paths = claude_md_files()
    if not paths:
        report.fail("claude-md-missing", "CLAUDE.md", "no CLAUDE.md anywhere in the repo")
        return

    for path in paths:
        r = rel(path)
        # .claude/CLAUDE.md documents the harness and is not part of the vault tier system.
        if r == ".claude/CLAUDE.md":
            continue
        text = read_text(path)
        size = len(text.encode("utf-8"))
        tier = tier_of(path, paths)

        if tier == "root":
            cap, warn_at, required = budgets["rootMaxBytes"], budgets["rootWarnBytes"], REQUIRED_ROOT_SECTIONS
        elif tier == "router":
            cap, warn_at, required = budgets["routerMaxBytes"], budgets["routerMaxBytes"], []
        else:
            cap, warn_at, required = budgets["leafMaxBytes"], budgets["leafWarnBytes"], REQUIRED_LEAF_SECTIONS

        if size > cap:
            report.fail("claude-md-budget", r,
                        "%s tier is %d B, cap %d B" % (tier, size, cap),
                        "Move the detail into linked docs and add rows to the "
                        "'| File | When to load |' table. A leaf CLAUDE.md is a router "
                        "into context, not the context.")
        elif size > warn_at:
            report.warn("claude-md-budget", r, "%s tier is %d B, soft target %d B" % (tier, size, warn_at))

        # Match an actual heading, not prose that names the prohibition. The
        # root CLAUDE.md states this rule, and stating it must not violate it.
        has_standards_heading = any(
            line.strip().startswith(PROHIBITED_CLAUDE_SECTION)
            for line in strip_code_fences(text).split("\n")
        )
        if has_standards_heading:
            report.fail("claude-md-standards-section", r,
                        "carries a '## Standards' section",
                        "Standards are stated once in Standards/ and routed by .claude/rules/ "
                        "globs that load on demand. A Standards heading here pays the always-on "
                        "price for something conditional.")

        if not template_mode:
            for section in required:
                if section not in text:
                    report.fail("claude-md-section", r, "%s tier is missing '%s'" % (tier, section))


# --------------------------------------------------------------------------
# Checks: links, placeholders, identity, purity
# --------------------------------------------------------------------------

def check_links(report: Report) -> None:
    md_files = [p for p in walk_mutate_surface() if p.suffix == ".md"]
    note_stems = {p.stem for p in REPO_ROOT.rglob("*.md")
                  if not any(part in MUTATE_IGNORE_DIRS for part in p.parts)}

    for path in md_files:
        r = rel(path)
        if r.startswith(".claude/rules/"):
            continue  # covered with anchor checking in check_rules
        text = read_text(path)
        for _, target in links_of(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = target.partition("#")[0]
            if not target_path:
                continue
            resolved = (path.parent / target_path).resolve()
            if not resolved.exists():
                report.fail("link-dead", r, "link target does not resolve: %s" % target)
        for match in WIKILINK_RE.finditer(strip_code_fences(text)):
            note = match.group(1).strip()
            if note and Path(note).stem not in note_stems:
                report.warn("wikilink-dead", r, "wikilink has no matching note: [[%s]]" % note)


def check_placeholders(report: Report, template_mode: bool) -> None:
    if template_mode:
        return  # before bootstrap, sentinels and tokens are the design working
    for path in walk_mutate_surface():
        r = rel(path)
        text = read_text(path)
        if SENTINEL in text:
            report.fail("sentinel-survived", r, "contains %s" % SENTINEL,
                        "A human or agent must supply this value before the workspace is done.")
        m = TOKEN_RE.search(text)
        if m:
            report.fail("token-survived", r, "contains unreplaced identity token %s" % m.group(0))
        if AGENT_COMMENT_RE.search(text):
            report.fail("agent-comment-survived", r, "contains an unresolved <!-- AGENT: --> instruction",
                        "The authoring pass replaces the slot and deletes the comment.")


def check_identity(report: Report) -> None:
    for path in walk_mutate_surface():
        r = rel(path)
        if r.startswith(IDENTITY_EXEMPT_PREFIXES):
            continue
        lowered = read_text(path).lower()
        for term in IDENTITY_TERMS:
            if term in lowered:
                report.fail("identity-leak", r,
                            "contains the identity term '%s'" % term,
                            "A template must not ship one consumer's identity. Parameterize it.")
                break


def check_template_purity(report: Report, config: Dict[str, object]) -> None:
    if config.get("bootstrapped"):
        return
    for path in all_repo_files():
        r = rel(path)
        if path.suffix != ".md":
            continue
        if r in TEMPLATE_CONTENT_WHITELIST or r.startswith(TEMPLATE_CONTENT_WHITELIST_DIRS):
            continue
        # A README explains a folder; it is scaffolding, not content. Notes that
        # would leak are never named README.md.
        if path.name == "README.md":
            continue
        report.fail("template-impure", r,
                    "workspace content in an un-bootstrapped template",
                    "This repo is public. Client notes must never reach it.")


def check_obsidian(report: Report) -> None:
    obsidian = REPO_ROOT / ".obsidian"
    if not obsidian.is_dir():
        return
    enabled_path = obsidian / "community-plugins.json"
    plugins_dir = obsidian / "plugins"
    if enabled_path.exists() and plugins_dir.is_dir():
        try:
            enabled = json.loads(read_text(enabled_path))
        except json.JSONDecodeError:
            report.fail("obsidian-json", rel(enabled_path), "is not valid JSON")
            enabled = []
        for plugin_id in enabled if isinstance(enabled, list) else []:
            pdir = plugins_dir / plugin_id
            if not pdir.is_dir():
                report.fail("obsidian-plugin-missing", rel(enabled_path),
                            "enables '%s' but .obsidian/plugins/%s does not exist" % (plugin_id, plugin_id),
                            "A fresh clone would show a broken plugin. Vendor its built files.")
                continue
            for required in ("main.js", "manifest.json"):
                if not (pdir / required).exists():
                    report.fail("obsidian-plugin-incomplete", rel(pdir),
                                "missing %s" % required)
    if plugins_dir.is_dir():
        for pdir in sorted(d for d in plugins_dir.iterdir() if d.is_dir()):
            if (pdir / "data.json.example").exists() and not (pdir / "SETUP.md").exists():
                report.fail("obsidian-setup-doc", rel(pdir),
                            "ships data.json.example but no SETUP.md",
                            "Per-machine config needs a documented one-time copy step.")


def check_gitignore(report: Report) -> None:
    """The .credentials un-ignore pattern is order-dependent and fragile."""
    if not (REPO_ROOT / ".gitignore").exists():
        return
    expectations = [
        (".credentials/README.md", False),
        (".credentials/github/tokens.env.example", False),
        (".credentials/github/tokens.env", True),
        (".obsidian/plugins/icloud-sync/data.json", True),
        (".obsidian/workspace.json", True),
        (".obsidian/community-plugins.json", False),
        (".obsidian/appearance.json", False),
    ]
    for candidate, should_be_ignored in expectations:
        proc = subprocess.run(["git", "check-ignore", "-q", candidate],
                              cwd=str(REPO_ROOT), capture_output=True)
        ignored = proc.returncode == 0
        if ignored != should_be_ignored:
            want = "ignored" if should_be_ignored else "tracked"
            report.fail("gitignore", ".gitignore",
                        "%s is %s but should be %s" % (candidate, "ignored" if ignored else "tracked", want))


def check_agents(report: Report) -> None:
    agents_dir = REPO_ROOT / ".claude" / "agents"
    if not agents_dir.is_dir():
        return
    for path in sorted(agents_dir.glob("*.md")):
        fm, _ = parse_frontmatter(read_text(path))
        if fm is None:
            report.fail("agent-frontmatter", rel(path), "no frontmatter")
            continue
        for key in ("name", "description", "tools"):
            if key not in fm:
                report.fail("agent-frontmatter", rel(path), "missing '%s'" % key)


def check_house_style(report: Report) -> None:
    for path in walk_mutate_surface():
        if path.suffix != ".md":
            continue
        r = rel(path)
        if r.startswith((".workspace/", "Decisions/")) or r == "THIRD-PARTY-NOTICES.md":
            continue
        body = strip_code_fences(read_text(path))
        body = re.sub(r"`[^`]*`", "", body)
        if "—" in body:
            report.warn("house-style-emdash", r, "contains an em dash")
        if re.search(r"[\U0001F300-\U0001FAFF✀-➿]", body):
            report.warn("house-style-emoji", r, "contains an emoji")


# --------------------------------------------------------------------------
# validate
# --------------------------------------------------------------------------

def run_validate(structure_only: bool = False, as_json: bool = False) -> int:
    config = load_config()
    budgets = budgets_from(config)
    template_mode = not bool(config.get("bootstrapped"))

    report = Report()
    check_rules(report, budgets, template_mode)
    check_registry(report)
    check_skills(report, budgets)
    check_claude_md(report, budgets, template_mode)
    check_links(report)
    if not structure_only:
        check_placeholders(report, template_mode)
    check_identity(report)
    check_template_purity(report, config)
    check_obsidian(report)
    check_gitignore(report)
    check_agents(report)
    check_house_style(report)

    if as_json:
        print(json.dumps({
            "bootstrapped": bool(config.get("bootstrapped")),
            "findings": [f.__dict__ for f in report.findings],
        }, indent=2))
        return 1 if report.failures else 0

    mode = "template (warn-only for placeholders)" if template_mode else "strict"
    print("workspace validate  ---  mode: %s" % mode)
    print("")
    if not report.findings:
        print("  clean. no findings.")
        return 0

    for level in (FAIL, WARN):
        group = [f for f in report.findings if f.level == level]
        if not group:
            continue
        mark = "x" if level == FAIL else "!"
        print("  %s %s (%d)" % (mark, level, len(group)))
        for f in group:
            print("      %-28s %s" % (f.code, f.path))
            print("        %s" % f.message)
            if f.hint:
                print("        -> %s" % f.hint)
        print("")

    print("  %d failing, %d warning" % (len(report.failures), len(report.warnings)))
    return 1 if report.failures else 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def not_yet(name: str) -> int:
    print("`%s` is not implemented yet. See .workspace/docs/ for the design." % name, file=sys.stderr)
    return 2


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="workspace", description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command")

    p_validate = sub.add_parser("validate", help="run the gate")
    p_validate.add_argument("--structure-only", action="store_true",
                            help="skip the placeholder grammars (for CI fixture renders)")
    p_validate.add_argument("--json", dest="as_json", action="store_true")

    p_bootstrap = sub.add_parser("bootstrap", help="turn this template into a workspace")
    p_bootstrap.add_argument("--plan")
    p_bootstrap.add_argument("--dry-run", action="store_true")
    p_bootstrap.add_argument("--force", action="store_true")
    p_bootstrap.add_argument("--overwrite-authored", action="store_true")

    p_add = sub.add_parser("add", help="scaffold one new area")
    p_add.add_argument("--parent", required=True)
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--role", default="leaf", choices=["leaf", "router", "note"])
    p_add.add_argument("--template")
    p_add.add_argument("--dry-run", action="store_true")

    p_render = sub.add_parser("render", help="re-render managed blocks from plan.json")
    p_render.add_argument("--only")
    p_render.add_argument("--dry-run", action="store_true")

    sub.add_parser("obsidian-setup", help="write per-machine plugin config from .example files")

    p_doctor = sub.add_parser("doctor", help="report template drift")
    p_doctor.add_argument("--upstream", action="store_true")
    p_doctor.add_argument("--vendored", action="store_true")

    p_upgrade = sub.add_parser("upgrade", help="pull a newer template into this workspace")
    p_upgrade.add_argument("--to", required=True)
    p_upgrade.add_argument("--dry-run", action="store_true")

    args = parser.parse_args(argv)
    if args.command == "validate":
        return run_validate(structure_only=args.structure_only, as_json=args.as_json)
    if args.command is None:
        parser.print_help()
        return 0
    return not_yet(args.command)


if __name__ == "__main__":
    sys.exit(main())
