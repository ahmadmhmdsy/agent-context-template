"""Install the context pack into a target repository. Adds; never modifies.

  adopt.py --target DIR [--components a,b] [--modules research,data]
           [--profile shared-tree|branch-per-agent] [--drop-rules 05,07]
           [--force] [--apply] [--allow-placeholders] [--json]

An existing target file is never overwritten: it is skipped and reported.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _packmodel as pm
from _mdtable import TableError, find_tables, replace_table

PACK_ROOT = Path(__file__).resolve().parent.parent

SKIP_TOP = pm.SKIP_TOP   # one home, in _packmodel.py; see the note there
SKIP_REL = ("docs/handoff", "docs/tasks", "docs/memory", "docs/.locks")

SEED_HANDOFF = """# Handoff

Newest entry first. Each entry starts with an ISO-8601 timestamp and offset.

<!-- rotate:begin -->
## 2026-01-01T00:00:00+00:00 — ADAPT

- **State:** ADAPT
- **Did:** ADAPT
- **Verified:** ADAPT (PASS | FAIL | SKIPPED)
- **Unverified / open:** ADAPT
- **Next:** ADAPT
- **Blockers:** ADAPT
- **Artifacts:** ADAPT
<!-- rotate:end -->

Rotated to `docs/handoff/archive-YYYY.md`. Rotation moves; it never deletes.
"""

SEED_TASKS = """# Tasks

Live rows only. Column order is fixed by `docs/00-schema.md`.

<!-- rotate:begin -->
| id | title | status | owner | scope | gate | evidence |
|---|---|---|---|---|---|---|
| T-1 | ADAPT | pending | ADAPT | ADAPT | - | - |
<!-- rotate:end -->

Completed rows rotate to `docs/tasks/archive-YYYY.md`.
"""

SEED_MEMORY = """# Memory -- topic registry

This registry lists topics, never individual lessons.

| topic | shard | entries | date range | last updated |
|---|---|---|---|---|
| general | `docs/memory/general.md` | 0 | - | ADAPT |
"""

SEED_SHARD = """# Lessons -- general

Oldest first. Status values come from `docs/00-schema.md`.

## ADAPT-<timestamp+offset> ADAPT

- **Status:** observed
- **Lesson:** ADAPT
- **Evidence:** ADAPT
"""

# Every path in a seed is a path the *target* repository's validator will read, so
# each one has to be written the way the shipped docs write it: root-relative, in a
# code span, never as a Markdown link. check_path_refs runs MD_LINK.sub(" ", body)
# before it looks for a reference, so a link hides its own target from the one check
# that resolves paths -- the same reason the live registry writes its shard cell bare.
SEEDS = {
    "docs/03-handoff.md": SEED_HANDOFF,
    "docs/04-tasks.md": SEED_TASKS,
    "docs/05-memory.md": SEED_MEMORY,
    "docs/memory/general.md": SEED_SHARD,
}


def module_number(name: str) -> str:
    m = re.match(r"^(\d{2})-", name)
    return m.group(1) if m else ""


def pack_files():
    for p in sorted(PACK_ROOT.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(PACK_ROOT)
        if rel.parts and rel.parts[0] in SKIP_TOP:
            continue
        key = str(rel).replace(chr(92), "/")
        if key.startswith(SKIP_REL) or p.suffix == ".pyc" or p.name.endswith(".tmp"):
            continue
        yield rel


def plan(target, drop_rules, components, modules):
    actions = []
    for rel in pack_files():
        key = str(rel).replace(chr(92), "/")
        if rel.parts[0] == "rules" and module_number(rel.name) in drop_rules:
            actions.append(("drop", key, "rule module declared inapplicable"))
            continue
        if rel.parts[0] == "modules" and (len(rel.parts) < 2 or rel.parts[1] not in modules):
            actions.append(("drop", key, "module not requested"))
            continue
        if (target / rel).exists():
            actions.append(("skip", key, "target file already exists"))
        else:
            actions.append(("copy", key, ""))
    for key in SEEDS:
        if (target / key).exists():
            actions.append(("skip", key, "target file already exists"))
        else:
            actions.append(("seed", key, "state seeded with one ADAPT entry"))
    for cid in components:
        for key in ("%s/AGENTS.md" % cid, "rules/components/%s.md" % cid):
            if (target / key).exists():
                actions.append(("skip", key, "target file already exists"))
            else:
                actions.append(("create", key, "component skeleton"))
    return actions


def apply_plan(target, actions, components, modules, profile, drop_rules):
    written = []
    for kind, key, _ in actions:
        if kind == "drop":
            continue
        dest = target / key
        dest.parent.mkdir(parents=True, exist_ok=True)
        if kind == "copy":
            shutil.copyfile(PACK_ROOT / key, dest)
            written.append(key)
        elif kind == "seed":
            dest.write_text(SEEDS[key], encoding="utf-8", newline="\n")
            written.append(key)
        elif kind == "create":
            if key.endswith("AGENTS.md"):
                body = (PACK_ROOT / "_templates" / "component-agents.md").read_text(encoding="utf-8")
            else:
                body = "# Component rule: %s\n\nADAPT\n" % Path(key).stem
            dest.write_text(body, encoding="utf-8", newline="\n")
            written.append(key)
    if components:
        add_component_rows(target, components)
    coord = target / "docs" / "08-coordination.md"
    if coord.is_file():
        text = coord.read_text(encoding="utf-8")
        text = text.replace("SHARED TREE", profile.upper().replace("-", " "), 1)
        coord.write_text(text, encoding="utf-8", newline="\n")
    if drop_rules:
        drop_index_rows(target, drop_rules)
    return written


def add_component_rows(target, components):
    path = target / "AGENTS.md"
    text = path.read_text(encoding="utf-8")
    try:
        table = next((t for t in find_tables(text) if t.has("id")), None)
    except TableError:
        return
    if not table:
        return
    rows = list(table.rows)
    have = {r.get("id", "") for r in rows}
    for cid in components:
        if cid in have:
            continue
        rows.append({"id": cid, "path scope": "%s/" % cid, "scoped entry": "%s/AGENTS.md" % cid,
                     "component rule": "rules/components/%s.md" % cid})
    path.write_text(replace_table(text, table, rows), encoding="utf-8", newline="\n")


def drop_index_rows(target, drop_rules):
    path = target / "rules" / "00-index.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    try:
        tables = find_tables(text)
    except TableError:
        return
    for t in tables:
        if not t.rows:
            continue
        col = next((h for h in t.header if re.search(r"module|id|no", h, re.I)), None)
        if not col:
            continue
        keep = [r for r in t.rows if module_number(r.get(col, "")) not in drop_rules]
        if len(keep) != len(t.rows):
            text = replace_table(text, t, keep)
    path.write_text(text, encoding="utf-8", newline="\n")


def placeholders(target):
    counts = {}
    for p in sorted(target.rglob("*.md")):
        rel = str(p.relative_to(target)).replace(chr(92), "/")
        if rel.split("/")[0] in SKIP_TOP:
            continue
        n = p.read_text(encoding="utf-8", errors="replace").count("ADAPT")
        if n:
            counts[rel] = n
    return counts


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Install the context pack into a target repository.")
    ap.add_argument("--target", required=True)
    ap.add_argument("--components", default="")
    ap.add_argument("--modules", default="")
    ap.add_argument("--profile", default="shared-tree", choices=("shared-tree", "branch-per-agent"))
    ap.add_argument("--drop-rules", default="")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--allow-placeholders", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    target = Path(args.target).resolve()
    if not target.is_dir():
        print("ERROR: target %s is not a directory" % target, file=sys.stderr)
        return 2
    version = PACK_ROOT / "VERSION"
    if not version.is_file():
        print("ERROR: %s is missing; every adopted tree is stamped with it, and reading it "
              "after the copy would leave a half-adopted target behind" % version, file=sys.stderr)
        return 2
    pack_version = version.read_text(encoding="utf-8").strip()
    if (target / "AGENTS.md").exists() and not args.force:
        print("ERROR: %s already has an AGENTS.md; refusing. Re-run with --force to add anyway." % target,
              file=sys.stderr)
        return 2
    components = [c.strip() for c in args.components.split(",") if c.strip()]
    modules = {m.strip() for m in args.modules.split(",") if m.strip()}
    drop = {d.strip() for d in args.drop_rules.split(",") if d.strip()}
    protected = sorted(drop & pm.PROTECTED_RULES)
    if protected:
        print("ERROR: rule modules are protected and cannot be dropped: %s" % ", ".join(protected), file=sys.stderr)
        return 2
    if not (target / ".git").exists():
        print("NOTE: %s is not a git repository; adoption is easier to undo where it is one." % target, file=sys.stderr)
    actions = plan(target, drop, components, modules)
    written = apply_plan(target, actions, components, modules, args.profile, drop) if args.apply else []
    counts = placeholders(target) if args.apply else {}
    if args.apply:
        (target / "context-pack.json").write_text(json.dumps({
            "pack": "context-pack",
            "pack_version": pack_version,
            "adopted_at": date.today().isoformat(),
            "components": components, "modules": sorted(modules),
            "profile": args.profile, "dropped_rules": sorted(drop),
        }, indent=2) + "\n", encoding="utf-8")
    summary = {
        "target": str(target), "applied": bool(args.apply), "profile": args.profile,
        "components": components, "modules": sorted(modules), "dropped_rules": sorted(drop),
        "written": len(written),
        "copy": sum(1 for k, _, _ in actions if k == "copy"),
        "skip": sum(1 for k, _, _ in actions if k == "skip"),
        "seed": sum(1 for k, _, _ in actions if k == "seed"),
        "create": sum(1 for k, _, _ in actions if k == "create"),
        "placeholders": counts,
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        for kind, key, why in actions:
            if kind in ("drop", "skip", "create"):
                print("%-7s %-46s %s" % (kind, key, why))
        print("%d to copy, %d skipped, %d seeded, %d created"
              % (summary["copy"], summary["skip"], summary["seed"], summary["create"]))
        for rel, n in sorted(counts.items()):
            print("ADAPT   %-46s %d" % (rel, n))
    if args.apply and counts and not args.allow_placeholders:
        print("ERROR: %d file(s) still contain ADAPT placeholders" % len(counts), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
