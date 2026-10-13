#!/usr/bin/env python3
"""Validate an agent context pack for structural drift.

Stdlib only. Run from the repository root, or pass one as the first argument:

    python scripts/validate_context.py .
    python scripts/validate_context.py /path/to/repo

Checks:
  1. Required files exist.
  2. CLAUDE.md and AGENTS.md cross-reference each other.
  3. Every rules module named in CLAUDE.md and rules/00-index.md exists.
  4. Every path-looking reference in the entry files and docs/ resolves.
  5. Every docs/ file declares a **Contract** block.
  6. The entry surface is within the boot budget.
  7. Reports remaining ADAPT markers per file.

Exit code 0 if no errors, 1 if any error was found. Warnings do not fail.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ENTRY_FILES = ("AGENTS.md", "CLAUDE.md")
BOOT_BUDGET_BYTES = 24576

REQUIRED = (
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    "rules/00-index.md",
    "docs/01-project.md",
    "docs/02-environment.md",
    "docs/03-handoff.md",
    "docs/04-tasks.md",
    "docs/05-memory.md",
    "docs/06-glossary.md",
    "docs/07-sources-of-truth.md",
    "docs/08-coordination.md",
    "docs/09-decisions/README.md",
    "docs/10-runbooks/README.md",
    "_templates/README.md",
)

PATH_REF = re.compile(r"(?<![\w/.\-])((?:rules|docs|_templates|scripts)/[A-Za-z0-9_./\-]*\.(?:md|py))")
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
ADAPT = re.compile(r"\bADAPT\b")

errors: list[str] = []
warnings: list[str] = []
info: list[str] = []


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        errors.append("cannot read %s: %s" % (path, exc))
        return ""


def check_required(root: Path) -> None:
    for rel in REQUIRED:
        if not (root / rel).is_file():
            errors.append("missing required file: %s" % rel)


def check_entry_crossref(root: Path) -> None:
    for name in ENTRY_FILES:
        p = root / name
        if not p.is_file():
            continue
        body = read(p)
        other = [n for n in ENTRY_FILES if n != name][0]
        if other not in body:
            errors.append("%s does not reference %s (entry files must cross-link)" % (name, other))


def check_rule_modules(root: Path) -> None:
    refs = set()
    for rel in ("CLAUDE.md", "rules/00-index.md"):
        p = root / rel
        if p.is_file():
            refs |= set(re.findall(r"rules/(\d{2}-[a-z0-9\-]+\.md)", read(p)))
    if not refs:
        errors.append("no rules modules referenced from CLAUDE.md or rules/00-index.md")
    for ref in sorted(refs):
        if not (root / "rules" / ref).is_file():
            errors.append("referenced rules module does not exist: rules/%s" % ref)
    files = sorted(p.name for p in (root / "rules").glob("[0-9][0-9]-*.md")) if (root / "rules").is_dir() else []
    for name in files:
        if name == "00-index.md":
            continue
        if name not in refs:
            warnings.append("rules/%s exists but is not indexed in CLAUDE.md or rules/00-index.md" % name)
    info.append("rules modules present: %d" % len(files))


def check_path_refs(root: Path) -> None:
    targets = [root / n for n in ENTRY_FILES]
    targets += sorted((root / "docs").rglob("*.md")) if (root / "docs").is_dir() else []
    targets += sorted((root / "rules").glob("*.md")) if (root / "rules").is_dir() else []
    for p in targets:
        if not p.is_file():
            continue
        body = read(p)
        text = MD_LINK.sub(" ", body)
        for ref in sorted(set(PATH_REF.findall(text))):
            ref = ref.rstrip(".,;:)")
            if "*" in ref or "?" in ref:
                continue
            if not (root / ref).exists():
                try:
                    rel = p.relative_to(root).as_posix()
                except ValueError:
                    rel = p.as_posix()
                errors.append("%s references a path that does not exist: %s" % (rel, ref))


def check_contracts(root: Path) -> None:
    docs = root / "docs"
    if not docs.is_dir():
        return
    missing = []
    for p in sorted(docs.rglob("*.md")):
        rel = p.relative_to(root).as_posix()
        if "/_" in rel or Path(rel).name.startswith("_"):
            continue
        if "0000-template" in rel:
            continue
        if "Contract" not in read(p):
            missing.append(rel)
    for rel in missing:
        warnings.append("%s does not declare a Contract block" % rel)


def check_budget(root: Path) -> None:
    total = 0
    for name in ENTRY_FILES:
        p = root / name
        if p.is_file():
            total += p.stat().st_size
    info.append("entry surface: %d bytes (budget %d)" % (total, BOOT_BUDGET_BYTES))
    if total > BOOT_BUDGET_BYTES:
        warnings.append(
            "entry surface is %d bytes, over the %d byte boot budget; move detail into rules/ or docs/"
            % (total, BOOT_BUDGET_BYTES)
        )


def report_adapt(root: Path) -> None:
    counts = []
    for p in sorted(root.rglob("*.md")):
        if any(part in (".git", "node_modules", ".venv") for part in p.parts):
            continue
        n = len(ADAPT.findall(read(p)))
        if n:
            try:
                rel = p.relative_to(root).as_posix()
            except ValueError:
                rel = p.as_posix()
            counts.append((n, rel))
    counts.sort(reverse=True)
    total = sum(n for n, _ in counts)
    info.append("ADAPT markers remaining: %d across %d files" % (total, len(counts)))
    for n, rel in counts[:15]:
        info.append("  %3d  %s" % (n, rel))


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not root.is_dir():
        print("not a directory: %s" % root)
        return 1

    check_required(root)
    check_entry_crossref(root)
    check_rule_modules(root)
    check_path_refs(root)
    check_contracts(root)
    check_budget(root)
    report_adapt(root)

    print("context pack: %s" % root)
    for line in info:
        print("  info   %s" % line)
    for line in warnings:
        print("  warn   %s" % line)
    for line in errors:
        print("  ERROR  %s" % line)
    print()
    print("result: %d error(s), %d warning(s)" % (len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
