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
from urllib.parse import unquote
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
    ".workspace/", ".credentials/", ".obsidian/",
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

        # The positive control, applied per RULE rather than per glob. A rule
        # listing several globs is not dead because one target folder is empty
        # or absent from this workspace's shape.
        live, dormant = [], []
        for pattern in paths:
            if not glob_is_supported(pattern):
                report.fail("rule-glob-syntax", r, "unsupported glob syntax: %s" % pattern,
                            "Supported: ** * ? [abc]. No braces, no negation, no extglob.")
                continue
            rx = glob_to_regex(pattern)
            if any(rx.match(c) for c in content_rels):
                live.append(pattern)
            else:
                dormant.append(pattern)
        # Does any directory a dormant glob targets actually exist? A folder
        # that exists and is empty will start routing as soon as content lands.
        existing_dirs = {str(d.relative_to(REPO_ROOT)) for d in REPO_ROOT.rglob("*")
                         if d.is_dir() and ".git" not in d.parts}
        target_exists = False
        for pattern in dormant:
            for seg in pattern.split("/"):
                if seg and "*" not in seg and "?" not in seg and "[" not in seg:
                    if any(d == seg or d.endswith("/" + seg) for d in existing_dirs):
                        target_exists = True
                        break
            if target_exists:
                break

        if not live and dormant and target_exists and not template_mode:
            report.warn("rule-glob-dormant", r,
                        "target folders exist but hold no matching file yet: %s"
                        % ", ".join(dormant),
                        "Normal in a young workspace. The rule starts routing when "
                        "content lands.")
        elif not live and dormant:
            msg = "no glob in this rule matches any file: %s" % ", ".join(dormant)
            if template_mode:
                report.warn("rule-glob-dead", r, msg,
                            "Expected before bootstrap: the target folders do not exist yet.")
            else:
                report.fail("rule-glob-dead", r, msg,
                            "The rule is unreachable. Either a folder was renamed without "
                            "rewriting these globs, or the rule no longer applies here and "
                            "should be removed along with its registry row.")
        elif dormant and not template_mode:
            report.warn("rule-glob-dormant", r,
                        "dormant globs (folder absent or empty): %s" % ", ".join(dormant),
                        "Fine while the area is unused. They start routing when content lands.")

        body = text[frontmatter_body_offset(text):]
        for label, target in links_of(body):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            target_path, _, anchor = target.partition("#")
            resolved = (path.parent / unquote(target_path)).resolve() if target_path else path
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


_PLAN_ROLES: Optional[Dict[str, str]] = None


def plan_roles() -> Dict[str, str]:
    """Declared role per node path, when a plan exists."""
    global _PLAN_ROLES
    if _PLAN_ROLES is None:
        _PLAN_ROLES = {}
        if PLAN_PATH.exists():
            try:
                for n in json.loads(read_text(PLAN_PATH)).get("nodes", []):
                    _PLAN_ROLES[n.get("path", "")] = n.get("role", "")
            except (json.JSONDecodeError, AttributeError):
                pass
    return _PLAN_ROLES


def tier_of(path: Path, all_paths: Sequence[Path]) -> str:
    """Root, router, or leaf.

    The plan is authoritative where it has an opinion: a router whose children
    are scaffold folders without their own CLAUDE.md is still a router, and
    judging it by structure alone reads it as a leaf and then demands leaf
    sections it should never have. Structure is the fallback.
    """
    if path.parent == REPO_ROOT:
        return "root"
    declared = plan_roles().get(rel(path.parent))
    if declared in ("router", "leaf"):
        return declared
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
        # These document the harness and the vault mechanics. Neither is an area,
        # so neither has a tier or the section skeleton that goes with one.
        if r in (".claude/CLAUDE.md", "Obsidian/CLAUDE.md"):
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
            resolved = (path.parent / unquote(target_path)).resolve()
            if not resolved.exists():
                report.fail("link-dead", r, "link target does not resolve: %s" % target)
            elif resolved.name not in os.listdir(resolved.parent):
                # macOS is case-insensitive, so a link whose case is wrong
                # resolves here and dangles on every Linux machine. The author
                # cannot see this class of bug without a check for it.
                report.fail("link-case", r,
                            "link resolves only on a case-insensitive filesystem: %s" % target,
                            "Match the file's real case. This dangles on Linux.")
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


def check_identity(report: Report, template_mode: bool) -> None:
    if not template_mode:
        return  # a workspace is supposed to carry its own identity
    for path in walk_mutate_surface():
        r = rel(path)
        if r.startswith(IDENTITY_EXEMPT_PREFIXES):
            continue
        text = read_text(path)
        # A provenance comment must name where it came from; that is the whole
        # point of it. Exempt the marker line itself rather than the whole file,
        # so identity leaking into the body is still caught.
        text = re.sub(r"<!--[^>]*?Vendored[^>]*?-->", "", text, flags=re.DOTALL)
        lowered = text.lower()
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
        # Plugins we deliberately do not vendor, because their license forbids it.
        # They are declared so the gate can tell "expected from the store" apart
        # from "someone enabled a plugin that is nowhere".
        store_ids = set()
        store_path = plugins_dir / "store-plugins.json"
        if store_path.exists():
            try:
                store_ids = {p["id"] for p in json.loads(read_text(store_path)).get("plugins", [])}
            except (json.JSONDecodeError, KeyError, TypeError):
                report.fail("obsidian-json", rel(store_path), "is not valid JSON")
        for plugin_id in enabled if isinstance(enabled, list) else []:
            pdir = plugins_dir / plugin_id
            if not pdir.is_dir():
                if plugin_id in store_ids:
                    continue  # installed from the store by `./workspace obsidian-setup`
                report.fail("obsidian-plugin-missing", rel(enabled_path),
                            "enables '%s' but it is neither vendored nor declared in store-plugins.json"
                            % plugin_id,
                            "Either vendor its built files, or declare it in "
                            ".obsidian/plugins/store-plugins.json with its license.")
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
        (".obsidian/plugins/agentic-copilot/data.json", True),
        (".obsidian/workspace.json", True),
        (".obsidian/community-plugins.json", False),
        (".obsidian/appearance.json", False),
        # A store plugin is a GPL or AGPL download. Once installed it sits in a
        # directory git would otherwise offer to stage, so the licensing
        # decision only holds if the ignore holds. The vendored pair beside it
        # must stay tracked, which is what rules out a blanket plugins ignore.
        (".obsidian/plugins/templater-obsidian/main.js", True),
        (".obsidian/plugins/obsidian-excalidraw-plugin/main.js", True),
        (".obsidian/themes/Things.css", True),
        (".obsidian/plugins/agentic-copilot/main.js", False),
        (".obsidian/plugins/icloud-sync/main.js", False),
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
# doctor and upgrade
# --------------------------------------------------------------------------

TEMPLATE_OWNED_PREFIXES = (".workspace", ".claude", "Obsidian/Templates", ".obsidian")


def template_owned_files() -> List[Path]:
    out = []
    for prefix in TEMPLATE_OWNED_PREFIXES:
        root = REPO_ROOT / prefix
        if not root.is_dir():
            continue
        for f in sorted(root.rglob("*")):
            if f.is_file() and ".git" not in f.parts and f.name != ".DS_Store":
                out.append(f)
    return out


def load_manifest() -> Dict[str, str]:
    path = REPO_ROOT / ".workspace" / "manifest.lock.json"
    if not path.exists():
        return {}
    try:
        return json.loads(read_text(path)).get("files", {})
    except json.JSONDecodeError:
        return {}


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_doctor(upstream: bool = False, vendored: bool = False) -> int:
    config = load_config()
    tmpl = config.get("template") or {}
    repo = tmpl.get("repo", "unknown")
    ref = tmpl.get("ref", "unknown")
    print("template  %s @ %s" % (repo, ref))
    if tmpl.get("bootstrappedAt"):
        print("          bootstrapped %s" % tmpl["bootstrappedAt"])
    print("")

    # Local divergence from the template. A file that differs will not receive
    # upgrades, which is the thing people are surprised by later.
    manifest = load_manifest()
    if not manifest:
        print("No manifest.lock.json, so local harness changes cannot be detected.")
        print("It is written at bootstrap and at every upgrade.")
    else:
        drifted, added, removed = [], [], []
        on_disk = {rel(f): f for f in template_owned_files()}
        for path, digest in sorted(manifest.items()):
            f = on_disk.get(path)
            if f is None:
                removed.append(path)
            elif sha256_of(f) != digest:
                drifted.append(path)
        for path in sorted(on_disk):
            if path not in manifest:
                added.append(path)
        if drifted:
            print("harness   %d template-owned file(s) diverge from %s:" % (len(drifted), ref))
            for path in drifted[:20]:
                print("            %s" % path)
            if len(drifted) > 20:
                print("            ... and %d more" % (len(drifted) - 20))
            print("          These will not receive upgrades. Port them upstream:")
            print("            gh repo clone %s" % repo)
        if added:
            print("local     %d file(s) added locally under template-owned paths" % len(added))
        if removed:
            print("missing   %d template-owned file(s) deleted locally" % len(removed))
        if not (drifted or added or removed):
            print("harness   clean, no divergence from the template")
    print("")

    if upstream:
        proc = subprocess.run(["gh", "release", "list", "--repo", repo, "--limit", "5"],
                              capture_output=True, text=True)
        if proc.returncode == 0 and proc.stdout.strip():
            print("upstream releases:")
            for line in proc.stdout.strip().split("\n"):
                print("  %s" % line)
            print("")
            print("  ./workspace upgrade --to <ref> --dry-run")
        else:
            print("upstream  could not list releases (is `gh` authenticated?)")
        print("")

    if vendored:
        print("vendored skills:")
        skills = REPO_ROOT / ".claude" / "skills"
        for d in sorted(skills.iterdir()) if skills.is_dir() else []:
            md = d / "SKILL.md"
            if not md.is_dir() and md.exists():
                text = read_text(md)
                m = VENDORED_ANY_RE.search(text)
                if not m:
                    continue
                sha = VENDORED_SHA_RE.search(text)
                url = m.group(1).rstrip(")").rstrip(",")
                verbatim = VENDORED_VERBATIM_MARKER in text
                print("  %-32s %-9s %s" % (d.name, "verbatim" if verbatim else "adapted",
                                           sha.group(1) if sha else "NO PIN"))
        print("")
        print("  A pin is what makes the manual diff against upstream tractable.")
    return 0


def run_upgrade(to_ref: str, dry_run: bool) -> int:
    """Replacement, not merge.

    A template repo shares no git history with the workspaces made from it, so
    there is nothing to merge. Replacement works only because template-owned
    paths hold no workspace content: that boundary is what this whole command
    rests on.
    """
    config = load_config()
    repo = (config.get("template") or {}).get("repo")
    if not repo:
        print("No template repo recorded in workspace.json.", file=sys.stderr)
        return 1

    manifest = load_manifest()
    if not manifest:
        print("No manifest.lock.json, so an unmodified file cannot be told from a", file=sys.stderr)
        print("modified one. Refusing to overwrite anything.", file=sys.stderr)
        return 1

    tmp = Path(os.environ.get("TMPDIR", "/tmp")) / ("awt-%s" % to_ref.replace("/", "-"))
    if tmp.exists():
        subprocess.run(["rm", "-rf", str(tmp)], check=False)
    print("fetching %s @ %s" % (repo, to_ref))
    proc = subprocess.run(["git", "clone", "--depth", "1", "--branch", to_ref,
                           "https://github.com/%s.git" % repo, str(tmp)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr.strip(), file=sys.stderr)
        return 1

    replace, conflict, added, gone = [], [], [], []
    for prefix in TEMPLATE_OWNED_PREFIXES:
        up_root = tmp / prefix
        if not up_root.is_dir():
            continue
        for up in sorted(up_root.rglob("*")):
            if not up.is_file() or ".git" in up.parts:
                continue
            r = str(up.relative_to(tmp))
            local = REPO_ROOT / r
            if not local.exists():
                added.append(r)
            elif r not in manifest:
                conflict.append(r)
            elif sha256_of(local) == manifest[r]:
                if sha256_of(up) != sha256_of(local):
                    replace.append(r)
            else:
                conflict.append(r)
    for r in manifest:
        if not (tmp / r).exists():
            gone.append(r)

    print("")
    for r in replace:
        print("  replace  %s" % r)
    for r in added:
        print("  add      %s" % r)
    for r in conflict:
        print("  keep     %s   (locally modified; diff against %s/%s)" % (r, tmp, r))
    for r in gone:
        print("  orphan   %s   (removed upstream; not deleted here)" % r)
    print("")
    print("  %d replace, %d add, %d kept as local, %d orphaned"
          % (len(replace), len(added), len(conflict), len(gone)))

    if dry_run:
        print("  next     ./workspace upgrade --to %s" % to_ref)
        return 0

    for r in replace + added:
        dst = REPO_ROOT / r
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((tmp / r).read_bytes())
    config.setdefault("template", {})["ref"] = to_ref
    CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    write_manifest_lock(False)
    print("")
    print("  Upgraded. Run ./workspace validate, then review the kept files above.")
    return 0

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
    check_identity(report, template_mode)
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
# Rendering: managed blocks, tokens, and the tree
# --------------------------------------------------------------------------

TEMPLATE_VERSION = "1"
TEMPLATES = REPO_ROOT / ".workspace" / "templates"

BLOCK_RE_TMPL = r"(<!--\s*workspace:%s:start\s*-->)(.*?)(<!--\s*workspace:%s:end\s*-->)"


def replace_managed_block(text: str, name: str, body: str) -> str:
    """Replace only what is between the fences, byte-preserving everything else.

    This is what makes a re-run a merge rather than a clobber, and it is why the
    folder map cannot drift: no human and no agent ever writes it.
    """
    pattern = re.compile(BLOCK_RE_TMPL % (name, name), re.DOTALL)
    if not pattern.search(text):
        return text
    return pattern.sub(lambda m: m.group(1) + "\n" + body.rstrip() + "\n" + m.group(3), text)


def load_plan(path: Optional[Path] = None) -> Dict[str, object]:
    target = path or PLAN_PATH
    if not target.exists():
        raise SystemExit("No plan at %s. Run `./workspace bootstrap` to create one." % target)
    return json.loads(read_text(target))


def rel_depth(node_path: str) -> str:
    """`..` repeated once per path segment, or `.` at the root.

    Computed rather than authored: a leaf four levels deep needs four levels of
    `..`, and an agent writing that from context gets it wrong often enough that
    every one of them becomes a dangling link that reads as correct.
    """
    depth = len([p for p in node_path.split("/") if p])
    return "/".join([".."] * depth) if depth else "."


def node_by_path(plan: Dict[str, object], path: str) -> Optional[Dict[str, object]]:
    for n in plan.get("nodes", []):
        if n.get("path") == path:
            return n
    return None


def parent_of(plan: Dict[str, object], node: Dict[str, object]) -> Optional[Dict[str, object]]:
    parts = node["path"].split("/")
    while len(parts) > 1:
        parts = parts[:-1]
        found = node_by_path(plan, "/".join(parts))
        if found:
            return found
    return None


def substitute(text: str, tokens: Dict[str, str]) -> str:
    for key, value in tokens.items():
        text = text.replace("{{%s}}" % key, value)
    return text


def identity_tokens(config: Dict[str, object], today: str) -> Dict[str, str]:
    people = config.get("people") or []
    primary = next((p for p in people if p.get("default")), people[0] if people else {})
    return {
        "WORKSPACE_NAME": str(config.get("workspaceName") or ""),
        "WORKSPACE_SLUG": str(config.get("slug") or ""),
        "WORKSPACE_DOMAIN": str(config.get("domain") or ""),
        "PRIMARY_EMAIL": str(config.get("primaryEmail") or ""),
        "SUPPORT_EMAIL": str(config.get("primaryEmail") or ""),
        "PRIMARY_OPERATOR": str(primary.get("display") or ""),
        "PRIMARY_OPERATOR_KEY": str(primary.get("key") or ""),
        "DAILY_NOTES_FOLDER": "Operators/%s/Daily Notes" % primary.get("key", "operator"),
        "TEMPLATE_VERSION": TEMPLATE_VERSION,
        "TODAY": today,
    }



def glob_target_segments(pattern: str) -> List[str]:
    """The literal directory names a glob targets, ignoring wildcards."""
    return [seg for seg in pattern.split("/")
            if seg and "*" not in seg and "?" not in seg and "[" not in seg
            and not seg.endswith(".md")]


def prune_unreachable_rules(plan: Dict[str, object], dry_run: bool, actions) -> List[str]:
    """Drop rules this workspace's shape can never reach, and their registry rows.

    A rule targeting Clients/ in a vault that has no clients is not drift, it is
    a rule for a shape you did not choose. Leaving it shipped would mean the
    registry claims coverage that does not exist, and the registry is the whole
    reason the rules layer can be trusted.

    Only rules whose target folders are absent ENTIRELY are pruned. A folder that
    exists and is merely empty keeps its rule: it starts routing when content
    lands.
    """
    # Union of what is on disk and what the plan will create. Reading disk alone
    # made a dry run disagree with the apply that follows it, which is worse than
    # being wrong in one direction: the whole protocol is "review the dry run,
    # then run the identical command".
    existing = {d.name for d in REPO_ROOT.rglob("*") if d.is_dir() and ".git" not in d.parts}
    for node in plan.get("nodes", []):
        for seg in node.get("path", "").split("/"):
            if seg:
                existing.add(seg)
        for seg in node.get("scaffold", []) + node.get("children", []):
            existing.add(seg)
    pruned = []
    for path in rule_files():
        fm, _ = parse_frontmatter(read_text(path))
        if not fm:
            continue
        patterns = fm.get("paths") or []
        reachable = False
        for pattern in patterns:
            segments = glob_target_segments(pattern)
            if not segments or any(seg in existing for seg in segments):
                reachable = True
                break
        if reachable:
            continue
        pruned.append(rel(path))
        actions.append(("prune", rel(path), "no target folder in this shape"))
        if not dry_run:
            path.unlink()

    if pruned and not dry_run and REGISTRY_PATH.exists():
        lines = read_text(REGISTRY_PATH).split("\n")
        kept, moved = [], []
        for line in lines:
            hit = next((r for r in pruned if "`%s`" % r in line), None)
            if hit and line.lstrip().startswith("|"):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                moved.append("- %s: %s" % (cells[0], cells[1]) if len(cells) > 1 else "- %s" % cells[0])
                continue
            kept.append(line)
        text = "\n".join(kept)
        if moved:
            text = text.replace("## Intentionally unrouted",
                                "## Not applicable to this workspace\n\n"
                                "Pruned at bootstrap: this workspace's shape has no folder these\n"
                                "standards govern. The standard still stands; nothing routes it here.\n\n"
                                + "\n".join(moved) + "\n\n## Intentionally unrouted")
        REGISTRY_PATH.write_text(text, encoding="utf-8")
    return pruned


def render_node_claude_md(plan, node, config, today, dry_run, actions):
    role = node.get("role")
    if role not in ("router", "leaf"):
        return
    target = REPO_ROOT / node["path"] / "CLAUDE.md"
    template = TEMPLATES / ("router.md" if role == "router" else "leaf.md")
    parent = parent_of(plan, node)
    tokens = identity_tokens(config, today)
    tokens.update({
        "NODE_PATH": node["path"],
        "NODE_TITLE": node.get("title", node["path"].split("/")[-1]),
        "NODE_PURPOSE": node.get("slots", {}).get("purpose", "__REPLACE_ME__"),
        "PARENT_TITLE": (parent or {}).get("title", "the workspace root"),
        "REL_TO_ROOT": rel_depth(node["path"]),
        "REL_TO_PARENT": rel_depth(node["path"].split("/")[-1]) if parent else rel_depth(node["path"]),
        "SCOPE": node["path"].lower(),
    })
    if target.exists():
        # Re-render managed blocks only; everything a human or an agent authored
        # outside the fences survives untouched.
        body = read_text(target)
        actions.append(("update", rel(target), "managed blocks"))
    else:
        body = substitute(read_text(template), tokens)
        actions.append(("create", rel(target), "%s  %d B" % (role, len(body.encode()))))
    if role == "router":
        body = replace_managed_block(body, "inventory", render_inventory(plan, node))
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")


def render_inventory(plan: Dict[str, object], node: Dict[str, object]) -> str:
    """A router's child list. Generated, so it cannot drift out of date."""
    prefix = node["path"] + "/"
    children = [n for n in plan.get("nodes", [])
                if n.get("path", "").startswith(prefix)
                and "/" not in n["path"][len(prefix):]]
    if not children:
        instance = node.get("instanceTemplate") or node.get("instanceRole")
        if instance:
            return "- Nothing here yet. Add one with `./workspace add --parent %s --name \"<name>\"`." % node["path"]
        return "- Nothing here yet."
    lines = []
    for child in children:
        name = child["path"].split("/")[-1]
        if child.get("role") in ("router", "leaf"):
            lines.append("- `%s/`: %s. Start at [`%s/CLAUDE.md`](%s/CLAUDE.md)."
                         % (name, child.get("title", name), name, name))
        else:
            lines.append("- `%s/`: %s." % (name, child.get("title", name)))
    return "\n".join(lines)


def render_root_map(plan: Dict[str, object]) -> str:
    top = [n for n in plan.get("nodes", []) if "/" not in n.get("path", "")]
    lines = ["| Folder | What it holds | Start here |", "|---|---|---|",
             "| `Standards/` | Every convention, stated once. Business-agnostic. | [`Standards/README.md`](Standards/README.md) |"]
    for n in top:
        path, title = n["path"], n.get("title", n["path"])
        if n.get("role") in ("router", "leaf"):
            start = "[`%s/CLAUDE.md`](%s/CLAUDE.md)" % (path, path)
        else:
            start = "[`%s/README.md`](%s/README.md)" % (path, path)
        lines.append("| `%s/` | %s | %s |" % (path, title, start))
    lines.append("| `Obsidian/` | Vault mechanics: guides and templates. Not content. | [`Obsidian/CLAUDE.md`](Obsidian/CLAUDE.md) |")
    lines.append("| `.claude/` | The agentic harness: rules, skills, agents, commands. | [`.claude/CLAUDE.md`](.claude/CLAUDE.md) |")
    return "\n".join(lines)


def render_home_nav(plan: Dict[str, object]) -> str:
    top = [n for n in plan.get("nodes", []) if "/" not in n.get("path", "")]
    out = ["## Conventions", "",
           "- [Standards](<Standards/README.md>) -- every convention, and the registry",
           "- [Context](<CONTEXT.md>) -- the ubiquitous language",
           "- [Decisions](<Decisions/README.md>) -- the decision register", ""]
    areas = [n for n in top if n.get("role") in ("router", "leaf")]
    if areas:
        out += ["## Areas", ""]
        out += ["- [%s](<%s/CLAUDE.md>)" % (n.get("title", n["path"]), n["path"]) for n in areas]
        out += [""]
    plain = [n for n in top if n.get("role") == "plain"]
    if plain:
        out += ["## Shared", ""]
        out += ["- [%s](<%s/README.md>)" % (n.get("title", n["path"]), n["path"]) for n in plain]
        out += [""]
    out += ["## How the vault works", "",
            "- [Obsidian guide](<Obsidian/Guide/00-obsidian-guide-index.md>)"]
    return "\n".join(out)


def scaffold_node(node, config, today, dry_run, actions):
    base = REPO_ROOT / node["path"]
    for sub in node.get("scaffold", []) + node.get("children", []):
        d = base / sub
        actions.append(("create", rel(d) + "/", "scaffold"))
        if not dry_run:
            d.mkdir(parents=True, exist_ok=True)
            (d / ".gitkeep").touch()
    if node.get("gitkeep") and not dry_run:
        base.mkdir(parents=True, exist_ok=True)
        (base / ".gitkeep").touch()
    tokens = identity_tokens(config, today)
    tokens.update({"NODE_TITLE": node.get("title", ""), "SCOPE": node["path"].lower(),
                   "TITLE": node.get("title", ""),
                   "REL_TO_ROOT": rel_depth(node["path"])})
    for spec in node.get("files", []):
        target = base / spec["name"]
        if target.exists():
            continue
        tpl = TEMPLATES / (spec["template"] + ".md")
        if not tpl.exists():
            continue
        actions.append(("create", rel(target), spec["template"]))
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(substitute(read_text(tpl), tokens), encoding="utf-8")


def apply_identity_tokens(config, today, dry_run, actions):
    tokens = identity_tokens(config, today)
    for path in walk_mutate_surface():
        body = read_text(path)
        new = substitute(body, tokens)
        if new != body:
            actions.append(("update", rel(path), "identity"))
            if not dry_run:
                path.write_text(new, encoding="utf-8")


def write_manifest_lock(dry_run: bool) -> None:
    """SHA-256 of every template-owned file, so `upgrade` can tell an untouched
    file from a locally-modified one and replace only the former."""
    if dry_run:
        return
    owned = []
    for prefix in (".workspace", ".claude", "Obsidian/Templates", ".obsidian"):
        root = REPO_ROOT / prefix
        if not root.is_dir():
            continue
        for f in sorted(root.rglob("*")):
            if f.is_file() and ".git" not in f.parts:
                owned.append(f)
    manifest = {}
    for f in owned:
        try:
            manifest[rel(f)] = hashlib.sha256(f.read_bytes()).hexdigest()
        except OSError:
            continue
    (REPO_ROOT / ".workspace" / "manifest.lock.json").write_text(
        json.dumps({"files": manifest}, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def print_actions(actions, plan, dry_run, next_cmd):
    verbs = {}
    for verb, path, note in actions:
        verbs[verb] = verbs.get(verb, 0) + 1
        print("  %-7s %-52s %s" % (verb, path, note))
    print("")
    budgets = budgets_from(load_config())
    sizes = {"root": [], "router": [], "leaf": []}
    paths = claude_md_files()
    for p in paths:
        if rel(p) == ".claude/CLAUDE.md":
            continue
        sizes[tier_of(p, paths)].append(len(read_text(p).encode()))
    print("  budgets  root %d/%d B   routers max %d/%d B   leaves max %d/%d B" % (
        max(sizes["root"] or [0]), budgets["rootMaxBytes"],
        max(sizes["router"] or [0]), budgets["routerMaxBytes"],
        max(sizes["leaf"] or [0]), budgets["leafMaxBytes"]))
    left = 0
    for p in walk_mutate_surface():
        t = read_text(p)
        left += t.count(SENTINEL) + len(AGENT_COMMENT_RE.findall(t))
    print("  authoring %d slots left for the authoring pass" % left)
    if dry_run:
        print("  next     %s" % next_cmd)


def run_bootstrap(plan_path=None, dry_run=False, force=False, overwrite_authored=False) -> int:
    config = load_config()
    if config.get("bootstrapped") and not force:
        print("This workspace is already bootstrapped.", file=sys.stderr)
        print("Re-run with --force to reconcile, or use `./workspace add` for one area.",
              file=sys.stderr)
        return 1

    if plan_path is None and not PLAN_PATH.exists():
        print("No plan yet. `./workspace bootstrap` with no --plan is the conversational")
        print("entry point: it hands off to Claude Code, which interviews you and writes")
        print(".workspace/plan.json. Run it from a terminal, or pass --plan directly.")
        return launch_conversation()

    plan = load_plan(Path(plan_path) if plan_path else None)
    today = os.environ.get("WORKSPACE_TODAY") or subprocess.run(
        ["date", "+%Y-%m-%d"], capture_output=True, text=True).stdout.strip()

    actions: List[Tuple[str, str, str]] = []
    for node in plan.get("nodes", []):
        if not dry_run:
            (REPO_ROOT / node["path"]).mkdir(parents=True, exist_ok=True)
        scaffold_node(node, config, today, dry_run, actions)
        render_node_claude_md(plan, node, config, today, dry_run, actions)
        if node.get("role") == "plain":
            readme = REPO_ROOT / node["path"] / "README.md"
            if not readme.exists():
                actions.append(("create", rel(readme), "plain"))
                if not dry_run:
                    readme.write_text("# %s\n\n%s\n" % (node.get("title", node["path"]),
                                                        node.get("slots", {}).get("purpose", "__REPLACE_ME__")),
                                      encoding="utf-8")

    # Managed blocks in the two files the engine owns outright.
    for target, block, body in ((REPO_ROOT / "CLAUDE.md", "map", render_root_map(plan)),
                                (REPO_ROOT / "Home.md", "nav", render_home_nav(plan))):
        if target.exists():
            text = read_text(target)
            new = replace_managed_block(text, block, body)
            if new != text:
                actions.append(("update", rel(target), "[%s block]" % block))
                if not dry_run:
                    target.write_text(new, encoding="utf-8")

    pruned = prune_unreachable_rules(plan, dry_run, actions)
    apply_identity_tokens(config, today, dry_run, actions)

    if not dry_run:
        config["bootstrapped"] = True
        config.setdefault("template", {})["bootstrappedAt"] = today
        CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        if plan_path:
            PLAN_PATH.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
        write_manifest_lock(dry_run)
        subprocess.run(["git", "config", "core.hooksPath", ".githooks"],
                       cwd=str(REPO_ROOT), capture_output=True)

    header = "[dry-run] " if dry_run else ""
    print("%splan %s -- %d nodes" % (header, plan_path or rel(PLAN_PATH), len(plan.get("nodes", []))))
    print("")
    cmd = "./workspace bootstrap --plan %s" % (plan_path or rel(PLAN_PATH))
    print_actions(actions, plan, dry_run, cmd)
    if pruned:
        print("")
        print("  %d rule(s) pruned: this shape has no folder they govern. Their standards" % len(pruned))
        print("  are listed under 'Not applicable' in Standards/README.md, so the registry")
        print("  stays true about what is actually routed here.")
    if not dry_run:
        print("")
        print("  Next: fill every __REPLACE_ME__ and act on every <!-- AGENT: --> comment,")
        print("  then run ./workspace validate. Do not commit until it passes.")
    return 0


def launch_conversation() -> int:
    """Bootstrapping this template is a conversation, not a form."""
    try:
        os.execvp("claude", ["claude", "/bootstrap"])
    except OSError:
        print("`claude` is not on PATH.", file=sys.stderr)
        print("Install Claude Code, or write .workspace/plan.json by hand from one of",
              file=sys.stderr)
        print("the fixtures in .workspace/fixtures/ and run:", file=sys.stderr)
        print("  ./workspace bootstrap --plan .workspace/plan.json", file=sys.stderr)
        return 1
    return 0


def run_add(parent: str, name: str, role: str, template: Optional[str], dry_run: bool) -> int:
    config = load_config()
    if not config.get("bootstrapped"):
        print("Bootstrap this workspace first; there is no plan to append to.", file=sys.stderr)
        return 1
    plan = load_plan()
    parent_node = node_by_path(plan, parent)
    if parent_node is None:
        print("No node at '%s'. Known top-level nodes: %s" % (
            parent, ", ".join(n["path"] for n in plan["nodes"] if "/" not in n["path"])),
            file=sys.stderr)
        return 1

    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    path = "%s/%s" % (parent, slug)
    if node_by_path(plan, path):
        print("'%s' already exists." % path, file=sys.stderr)
        return 1

    role = parent_node.get("instanceRole") or role
    template = template or parent_node.get("instanceTemplate") or ("leaf" if role == "leaf" else "router")
    node = {"path": path, "role": role, "title": name, "template": template}
    if role == "leaf":
        node["scaffold"] = ["Activities", "Documents"]
        node["files"] = [{"name": "%s - Parking Lot.md" % name, "template": "parking-lot"}]
        node["folderNote"] = "%s.md" % name

    today = subprocess.run(["date", "+%Y-%m-%d"], capture_output=True, text=True).stdout.strip()
    actions: List[Tuple[str, str, str]] = []
    if not dry_run:
        (REPO_ROOT / path).mkdir(parents=True, exist_ok=True)
        plan["nodes"].append(node)
    else:
        plan = json.loads(json.dumps(plan))
        plan["nodes"].append(node)

    scaffold_node(node, config, today, dry_run, actions)
    render_node_claude_md(plan, node, config, today, dry_run, actions)
    # The parent's inventory and the root map are regenerated, which is why they
    # cannot drift: nobody writes them by hand.
    render_node_claude_md(plan, parent_node, config, today, dry_run, actions)
    root = REPO_ROOT / "CLAUDE.md"
    if root.exists():
        text = read_text(root)
        new = replace_managed_block(text, "map", render_root_map(plan))
        if new != text:
            actions.append(("update", "CLAUDE.md", "[map block]"))
            if not dry_run:
                root.write_text(new, encoding="utf-8")

    if not dry_run:
        PLAN_PATH.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")

    print("%sadd %s under %s" % ("[dry-run] " if dry_run else "", name, parent))
    print("")
    print_actions(actions, plan, dry_run,
                  './workspace add --parent %s --name "%s"' % (parent, name))
    return 0


def run_render(only: Optional[str], dry_run: bool) -> int:
    config = load_config()
    plan = load_plan()
    today = subprocess.run(["date", "+%Y-%m-%d"], capture_output=True, text=True).stdout.strip()
    actions: List[Tuple[str, str, str]] = []
    for node in plan.get("nodes", []):
        if only and node["path"] != only:
            continue
        render_node_claude_md(plan, node, config, today, dry_run, actions)
    for target, block, body in ((REPO_ROOT / "CLAUDE.md", "map", render_root_map(plan)),
                                (REPO_ROOT / "Home.md", "nav", render_home_nav(plan))):
        if target.exists():
            text = read_text(target)
            new = replace_managed_block(text, block, body)
            if new != text:
                actions.append(("update", rel(target), "[%s block]" % block))
                if not dry_run:
                    target.write_text(new, encoding="utf-8")
    # operators.js is generated from workspace.json, which is what keeps every
    # template free of a person's name.
    ops_target = REPO_ROOT / "Obsidian" / "Templates" / "scripts" / "operators.js"
    if ops_target.exists():
        people = config.get("people") or []
        entries = ",\n    ".join(
            '{ key: "%s", display: "%s", default: %s }'
            % (p.get("key"), p.get("display"), "true" if p.get("default") else "false")
            for p in people)
        text = read_text(ops_target)
        new = re.sub(r"list: \(\) => \[\n.*?\n  \],", "list: () => [\n    %s\n  ]," % entries,
                     text, flags=re.DOTALL)
        if new != text:
            actions.append(("update", rel(ops_target), "operators"))
            if not dry_run:
                ops_target.write_text(new, encoding="utf-8")
    print("%srender" % ("[dry-run] " if dry_run else ""))
    print("")
    print_actions(actions, plan, dry_run, "./workspace render")
    return 0

# --------------------------------------------------------------------------
# obsidian-setup
# --------------------------------------------------------------------------

def obsidian_is_running() -> bool:
    """Obsidian rewrites plugin data.json from memory on quit.

    Editing those files while it is open means your edit is silently discarded
    the next time it saves, which is the single most confusing failure in this
    whole setup.
    """
    try:
        out = subprocess.run(["pgrep", "-f", "Obsidian.app/Contents/MacOS/Obsidian"],
                             capture_output=True, text=True)
        return out.returncode == 0 and out.stdout.strip() != ""
    except OSError:
        return False


def machine_tokens(config: Dict[str, object]) -> Dict[str, str]:
    home = str(Path.home())
    name = str(config.get("workspaceName") or REPO_ROOT.name)
    return {
        "{{HOME}}": home,
        "{{VAULT_NAME}}": name,
        "{{VAULT_PATH}}": str(REPO_ROOT),
        "{{ICLOUD_DOCS}}": os.path.join(
            home, "Library", "Mobile Documents", "iCloud~md~obsidian", "Documents"),
    }


def run_obsidian_setup(dry_run: bool = False) -> int:
    config = load_config()
    obsidian = REPO_ROOT / ".obsidian"
    if not obsidian.is_dir():
        print("No .obsidian directory. Nothing to set up.")
        return 0

    if obsidian_is_running() and not dry_run:
        print("Obsidian is running. Quit it first, then re-run this.", file=sys.stderr)
        print("It writes plugin config from memory on quit, so edits made now are lost.",
              file=sys.stderr)
        return 1

    tokens = machine_tokens(config)
    plugins_dir = obsidian / "plugins"
    wrote, skipped = [], []

    for example in sorted(plugins_dir.glob("*/data.json.example")):
        target = example.parent / "data.json"
        if target.exists():
            skipped.append(rel(target))
            continue
        body = read_text(example)
        for token, value in tokens.items():
            body = body.replace(token, value)
        # A path pasted from a shell carries backslash-escaped spaces, which get
        # stored verbatim and sync into a directory that does not exist. The
        # symptom is a sync that reports success and moves nothing.
        for line in body.split("\n"):
            if "\\ " in line:
                print("Refusing to write %s: a value contains an escaped space." % rel(target),
                      file=sys.stderr)
                print("  %s" % line.strip(), file=sys.stderr)
                print("Use the literal path, not one copied from a shell prompt.", file=sys.stderr)
                return 1
        if dry_run:
            print("  would write  %s" % rel(target))
        else:
            target.write_text(body, encoding="utf-8")
            print("  wrote        %s" % rel(target))
        wrote.append(rel(target))

    # Create any destination a plugin config points at, so first sync does not
    # fail on a missing directory. The plugin nests its config, so the key is
    # settings.icloudBasePath; reading the top level found nothing and skipped
    # the mkdir without saying so, which is invisible here and shows up later as
    # the failure this step exists to prevent, a sync that reports success and
    # moves nothing. A missing key is now said out loud rather than assumed away.
    icloud = plugins_dir / "icloud-sync" / "data.json"
    if icloud.exists() and not dry_run:
        try:
            data = json.loads(read_text(icloud))
        except json.JSONDecodeError:
            data = {}
        settings = data.get("settings")
        base = (settings if isinstance(settings, dict) else {}).get("icloudBasePath")
        if not base:
            print("  warning      %s has no settings.icloudBasePath, so no sync "
                  "destination was created" % rel(icloud), file=sys.stderr)
        elif not Path(base).exists():
            Path(base).mkdir(parents=True, exist_ok=True)
            print("  created      %s" % base)
        else:
            print("  kept         %s (destination exists)" % base)

    for path in skipped:
        print("  kept         %s (already configured)" % path)

    # Report what still has to happen in Obsidian itself.
    store_path = plugins_dir / "store-plugins.json"
    if store_path.exists():
        try:
            declared = json.loads(read_text(store_path))
        except json.JSONDecodeError:
            declared = {}
        missing = [p for p in declared.get("plugins", [])
                   if not (plugins_dir / p["id"]).is_dir()]
        themes = [t for t in declared.get("themes", [])
                  if not (obsidian / "themes" / t["name"]).is_dir()]
        if missing or themes:
            print("")
            print("Install these from Obsidian, Settings then Community plugins:")
            for p in missing:
                print("  %-26s %s  (%s)" % (p["name"], p["repo"], p["license"]))
            for t in themes:
                print("  %-26s %s  (theme)" % (t["name"], t["repo"]))
            print("")
            print("They are not committed because four of them are GPL or AGPL, and")
            print("redistributing copyleft binaries inside an MIT template is a license")
            print("violation. The enable-list already travels, so they switch on as soon")
            print("as they are installed.")

    print("")
    print("Then: open this folder in Obsidian as a vault and trust the plugins when asked.")
    print("A fresh clone with plugins disabled looks broken, so do not skip the prompt.")
    return 0

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

    p_obs = sub.add_parser("obsidian-setup", help="write per-machine plugin config from .example files")
    p_obs.add_argument("--dry-run", action="store_true")

    p_doctor = sub.add_parser("doctor", help="report template drift")
    p_doctor.add_argument("--upstream", action="store_true")
    p_doctor.add_argument("--vendored", action="store_true")

    p_upgrade = sub.add_parser("upgrade", help="pull a newer template into this workspace")
    p_upgrade.add_argument("--to", required=True)
    p_upgrade.add_argument("--dry-run", action="store_true")

    args = parser.parse_args(argv)
    if args.command == "doctor":
        return run_doctor(upstream=args.upstream, vendored=args.vendored)
    if args.command == "upgrade":
        return run_upgrade(args.to, args.dry_run)
    if args.command == "bootstrap":
        return run_bootstrap(args.plan, args.dry_run, args.force, args.overwrite_authored)
    if args.command == "add":
        return run_add(args.parent, args.name, args.role, args.template, args.dry_run)
    if args.command == "render":
        return run_render(args.only, args.dry_run)
    if args.command == "obsidian-setup":
        return run_obsidian_setup(dry_run=args.dry_run)
    if args.command == "validate":
        return run_validate(structure_only=args.structure_only, as_json=args.as_json)
    if args.command is None:
        parser.print_help()
        return 0
    return not_yet(args.command)


if __name__ == "__main__":
    sys.exit(main())
