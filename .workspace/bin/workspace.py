#!/usr/bin/env python3
"""The workspace engine: structure generation.

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
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

CONFIG_PATH = REPO_ROOT / ".workspace" / "workspace.json"
PLAN_PATH = REPO_ROOT / ".workspace" / "plan.json"

# Identity substitution uses an UPPER-first {{TOKEN}} grammar. That anchor is
# deliberate and matters more here than in a code repo: Obsidian's own Templates
# plugin uses lowercase {{title}}, {{date:YYYY-MM-DD}}, {{time}}. Anchoring on an
# uppercase first character excludes that grammar by construction, along with JSX
# object expressions and Go/Hugo template syntax.
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
    """Every file identity substitution is allowed to rewrite.

    Keeping the walk and its exclusions in one function is what stops the
    exclusion list from being restated, and diverging, at each call site.
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
# Rules layer
# --------------------------------------------------------------------------

def rule_files() -> List[Path]:
    rules_dir = REPO_ROOT / ".claude" / "rules"
    if not rules_dir.is_dir():
        return []
    return sorted(p for p in rules_dir.rglob("*.md") if p.is_file())


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
    print("  Upgraded. Review the kept files above.")
    return 0


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
    """Drop rules this workspace's shape can never reach.

    A rule targeting Clients/ in a vault that has no clients is not drift, it is
    a rule for a shape you did not choose. Shipping it anyway means the rules
    layer claims coverage that does not exist.

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
           "- [Standards](<Standards/README.md>) -- every convention, stated once",
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

    header = "[dry-run] " if dry_run else ""
    print("%splan %s -- %d nodes" % (header, plan_path or rel(PLAN_PATH), len(plan.get("nodes", []))))
    print("")
    cmd = "./workspace bootstrap --plan %s" % (plan_path or rel(PLAN_PATH))
    print_actions(actions, plan, dry_run, cmd)
    if pruned:
        print("")
        print("  %d rule(s) pruned: this shape has no folder they govern. The standards" % len(pruned))
        print("  they routed still stand in Standards/; nothing routes them here.")
    if not dry_run:
        print("")
        print("  Next: fill every __REPLACE_ME__ and act on every <!-- AGENT: --> comment")
        print("  before you commit.")
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
    if args.command is None:
        parser.print_help()
        return 0
    return not_yet(args.command)


if __name__ == "__main__":
    sys.exit(main())
