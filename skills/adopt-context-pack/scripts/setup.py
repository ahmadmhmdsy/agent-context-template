#!/usr/bin/env python3
"""The mechanical half of the adopt-context-pack skill.

It never edits a project document (that needs judgement about the project) and
it never writes into a target unless --yes is passed. Run it, read the JSON,
then do the thinking it cannot do.

Subcommands:
  resolve     locate the pack, without touching anything
  preflight   what is in the target, what would collide, what the environment has
  install     drive the pack's own scripts/adopt.py (dry run unless --yes)
  markers     list the ADAPT markers left behind, split into homes and forms
  check       run the pack's validator against the target

Exit codes: 0 clean, 1 a finding worth acting on, 2 usage or internal error.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PACK_URL = "https://github.com/ahmadmhmdsy/agent-context-template.git"
MARKER = "ADAPT"
NOISE = {".git", ".venv", "venv", "__pycache__", "node_modules", ".pytest_cache", ".mypy_cache", ".locks", "skills"}

# The pack's own vocabulary: a marker inside a *form* is filled each time the
# form is used, so it is not a gap in the project's context. A marker anywhere
# else is a fact the project still has not written down.
FORM_DIRS = ("_templates",)
FORM_FILES = ("docs/09-decisions/0000-template.md", "docs/10-runbooks/_template.md")


def fail(msg: str, code: int = 2):
    print(json.dumps({"ok": False, "error": msg}, indent=2))
    raise SystemExit(code)


def run(cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def looks_like_pack(path: Path) -> bool:
    return (
        (path / "context-pack.json").is_file()
        and (path / "scripts" / "adopt.py").is_file()
        and (path / "AGENTS.md").is_file()
    )


def resolve_pack(args) -> tuple[Path, str]:
    """First source that answers wins; the order is deliberate."""
    if args.pack:
        p = Path(args.pack).expanduser().resolve()
        return (p, "argument") if looks_like_pack(p) else fail(f"--pack {p} is not a context pack (no context-pack.json + scripts/adopt.py + AGENTS.md)")
    env = os.environ.get("CONTEXT_PACK_HOME")
    if env:
        p = Path(env).expanduser().resolve()
        if looks_like_pack(p):
            return p, "env:CONTEXT_PACK_HOME"
    here = Path(__file__).resolve().parent
    for candidate in [here, *here.parents]:
        if looks_like_pack(candidate):
            return candidate, "skill-location"
    cache = Path(args.cache).expanduser() if args.cache else default_cache()
    if looks_like_pack(cache):
        if not args.no_clone and (cache / ".git").exists() and shutil.which("git"):
            # A cache that never refreshes pins every future adoption to one version,
            # so it is a cache: a fast-forward pull is the whole update policy.
            code, out, err = run(["git", "-C", str(cache), "pull", "--quiet", "--ff-only"])
            print(f"[setup] cache refresh: {'ok' if code == 0 else 'skipped'} {(err or '').strip()[:200]}", file=sys.stderr)
        return cache, "cache"
    if args.no_clone:
        fail(f"no pack found and cloning is disabled; set CONTEXT_PACK_HOME or pass --pack (tried {cache})")
    if not shutil.which("git"):
        fail("no pack found locally and git is not installed, so it cannot be fetched; pass --pack PATH or set CONTEXT_PACK_HOME")
    cache.parent.mkdir(parents=True, exist_ok=True)
    print(f"[setup] cloning {PACK_URL} -> {cache}", file=sys.stderr)
    code, out, err = run(["git", "clone", "--quiet", "--depth", "1", PACK_URL, str(cache)])
    if code != 0 or not looks_like_pack(cache):
        fail(f"git clone failed ({code}): {(err or out).strip()[:400]}")
    return cache, "clone"


def default_cache() -> Path:
    base = os.environ.get("LOCALAPPDATA") or os.environ.get("XDG_CACHE_HOME")
    root = Path(base) if base else Path.home() / ".cache"
    return root / "context-pack"


def pack_facts(pack: Path) -> dict:
    facts = {"path": str(pack)}
    manifest = pack / "context-pack.json"
    try:
        facts.update(json.loads(manifest.read_text(encoding="utf-8")))
    except Exception as exc:
        facts["manifest_error"] = str(exc)
    version = pack / "VERSION"
    if version.is_file():
        facts["version_file"] = version.read_text(encoding="utf-8").strip()
    facts["adopt"] = str(pack / "scripts" / "adopt.py")
    facts["validate"] = str(pack / "scripts" / "validate_context.py")
    return facts


def walk(root: Path):
    for path in sorted(root.rglob("*")):
        if path.is_dir():
            continue
        if any(part in NOISE for part in path.parts):
            continue
        yield path


def relative(root: Path, path: Path) -> str:
    return str(path.relative_to(root)).replace(os.sep, "/")


# Files that ship with the pack's own history already in them. Their markers are
# not facts to fill in - they are the pack's seeded state, and step 4 of the
# skill clears them. Reporting them as "homes" sends an adopter to write project
# facts into a record of someone else's project.
SEED = ("docs/03-handoff.md", "docs/04-tasks.md", "docs/05-memory.md", "docs/memory/",
        "docs/handoff/", "docs/tasks/")


def is_seed(rel: str) -> bool:
    return any(rel == s or rel.startswith(s) for s in SEED)


def is_form(rel: str) -> bool:
    return rel.startswith(FORM_DIRS) or rel in FORM_FILES or rel.endswith("_template.md")


def marker_rows(root: Path) -> list[dict]:
    rows = []
    for path in walk(root):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        # Markers are a Markdown convention, and the validator scans *.md; a script
        # that merely mentions the word is not an unfilled project fact.
        if path.suffix != ".md" or MARKER not in text:
            continue
        rel = relative(root, path)
        lines = [i for i, line in enumerate(text.splitlines(), 1) if MARKER in line]
        kind = "seed" if is_seed(rel) else ("form" if is_form(rel) else "home")
        rows.append({"file": rel, "count": len(lines), "lines": lines, "kind": kind})
    return rows


EXISTING = ["AGENTS.md", "CLAUDE.md", "GEMINI.md", "SOUL.md", ".github/copilot-instructions.md",
            ".cursor/rules/pack.mdc", "rules/00-index.md", "docs/00-schema.md", "docs/03-handoff.md",
            "scripts/adopt.py", "context-pack.json"]
LEGACY = ["HANDOFF.md", "MEMORY.md", "TASKS.md", "CURRENT_STATE.md", "PLAN.md", "ENVIRONMENT.md", ".cursorrules"]


def cmd_resolve(args):
    pack, source = resolve_pack(args)
    facts = pack_facts(pack)
    facts["source"] = source
    facts["pack_url"] = PACK_URL
    return {"ok": True, **facts}


def cmd_preflight(args):
    target = Path(args.target).resolve()
    if not target.is_dir():
        fail(f"target {target} is not a directory (adopt.py requires it to exist already)")
    pack, source = resolve_pack(args)
    present = [p for p in EXISTING if (target / p).exists()]
    legacy = [p for p in LEGACY if (target / p).exists()]
    inside = target != Path(__file__).resolve().parent and (target / "context-pack.json").is_file()
    facts = {
        "ok": True,
        "target": str(target),
        "pack": str(pack),
        "pack_source": source,
        "python": {"executable": sys.executable, "version": ".".join(map(str, sys.version_info[:3])), "ok": sys.version_info >= (3, 11)},
        "git": {"installed": bool(shutil.which("git")), "target_is_repo": (target / ".git").exists()},
        "pack_already_present": inside,
        "existing_pack_paths": present,
        "legacy_agent_files": legacy,
        "would_need_force": "AGENTS.md" in present,
    }
    if facts["would_need_force"]:
        facts["note"] = "AGENTS.md already exists, so adopt.py stops unless --force. Snapshot the target (git branch or a copy) and get the owner's consent before forcing; then reconcile rather than replace - see references/playbook.md."
    if legacy:
        facts["legacy_note"] = "This target already has an agent context system of its own. Map its content into the pack's homes instead of running both: two rule trees with no precedence rule is worse than one. See references/playbook.md."
    if not facts["python"]["ok"]:
        facts["python"]["note"] = "the pack needs Python 3.11+"
    if not facts["git"]["target_is_repo"]:
        facts["git"]["note"] = "not a git repository: nothing can be snapshotted or diffed, and the pack's own rules assume one"
    return facts


def adopt_argv(args, pack: Path) -> list[str]:
    target = Path(args.target).resolve()
    argv = [args.python or sys.executable, str(pack / "scripts" / "adopt.py"), "--target", str(target)]
    if args.components:
        argv += ["--components", args.components]
    if args.modules:
        argv += ["--modules", args.modules]
    if args.profile:
        argv += ["--profile", args.profile]
    if args.drop_rules:
        argv += ["--drop-rules", args.drop_rules]
    if args.force:
        argv.append("--force")
    argv.append("--allow-placeholders")
    argv.append("--json")
    if args.yes:
        argv.append("--apply")
    return argv


def extract_json(text: str):
    start = text.find("{")
    while start != -1:
        depth, in_str, escaped = 0, False, False
        for i in range(start, len(text)):
            ch = text[i]
            if in_str:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == '"':
                    in_str = False
                continue
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start:i + 1])
                    except json.JSONDecodeError:
                        break
        start = text.find("{", start + 1)
    return None


def git_status(target: Path):
    """The target's own view of what changed. A plan's numbers are not evidence."""
    if not (target / ".git").exists() or not shutil.which("git"):
        return None
    code, out, _ = run(["git", "status", "--porcelain"], cwd=target)
    return sorted(line for line in out.splitlines() if line.strip()) if code == 0 else None


def cmd_install(args):
    pack, source = resolve_pack(args)
    target = Path(args.target).resolve()
    if not target.is_dir():
        fail(f"target {target} is not a directory")
    argv = adopt_argv(args, pack)
    before = git_status(target)
    code, out, err = run(argv)
    after = git_status(target) if before is not None else None
    summary = extract_json(out) or extract_json(err)
    result = {
        "ok": code == 0,
        "applied": bool(args.yes) and code == 0,
        "command": " ".join(f'"{a}"' if " " in a else a for a in argv),
        "exit_code": code,
        "pack": str(pack),
        "pack_source": source,
        "adopt_summary": summary,
    }
    if before is not None and after is not None:
        observed = sorted(set(after) - set(before))
        result["observed_changes"] = observed
        result["observed_change_note"] = ("evidence, not accounting: the target's own git status before and after, "
                                          "so a plan whose numbers disagree with the tree is visible")
        if args.yes and code == 0 and not observed:
            result["warning"] = "adopt.py reported success but git saw no change in the target; check by hand"
    if code != 0:
        result["output_tail"] = (err or out).strip().splitlines()[-12:]
    elif not summary:
        result["output_tail"] = out.strip().splitlines()[-12:]
    if code != 0:
        result["error"] = "adopt.py failed; read output_tail. A refusal is a decision point, not a bug: do not add --force to silence it."
    elif not summary:
        result["note"] = "adopt.py produced no JSON summary; read output_tail for what it did"
    if args.yes:
        result["next"] = ["clear the inherited state (docs/03-handoff.md, docs/04-tasks.md, docs/05-memory.md, both archives)",
                          "run: setup.py markers --target TARGET", "resolve every marker whose kind is 'home'",
                          "run: setup.py check --target TARGET"]
    else:
        result["next"] = ["this was a dry run; re-run with --yes once the plan is right"]
    return result


def cmd_markers(args):
    target = Path(args.target).resolve()
    if not target.is_dir():
        fail(f"target {target} is not a directory")
    rows = marker_rows(target)
    homes = [r for r in rows if r["kind"] == "home"]
    forms = [r for r in rows if r["kind"] == "form"]
    seeds = [r for r in rows if r["kind"] == "seed"]
    return {
        "ok": True,
        "target": str(target),
        "marker": MARKER,
        "home_files": len(homes),
        "home_markers": sum(r["count"] for r in homes),
        "form_files": len(forms),
        "form_markers": sum(r["count"] for r in forms),
        "seed_files": len(seeds),
        "seed_markers": sum(r["count"] for r in seeds),
        "rows": rows,
        "note": ("home = a fact this project has not written yet; fill it, or write 'unknown', which is a decision. "
                 "seed = the pack's own history, which ships in these files; clear it (step 4) and re-run this "
                 "command - the count should drop. form = a template slot filled each time the form is used; leave it."),
    }


def cmd_check(args):
    target = Path(args.target).resolve()
    validator = target / "scripts" / "validate_context.py"
    if not validator.is_file():
        fail(f"{validator} not found: install the pack before checking it")
    argv = [args.python or sys.executable, str(validator), "--root", str(target)]
    if args.baseline:
        argv += ["--baseline", args.baseline]
    if args.write_baseline:
        argv += ["--write-baseline", args.write_baseline]
    if args.json:
        argv.append("--json")
    code, out, err = run(argv)
    text = (out or err).strip()
    markers = marker_rows(target)
    homes = [r for r in markers if r["kind"] == "home"]
    return {
        "ok": code == 0,
        "exit_code": code,
        "command": " ".join(argv),
        "output_tail": text.splitlines()[-25:],
        "home_markers_remaining": sum(r["count"] for r in homes),
        "note": ("exit 0 means no findings - but ADAPT markers are INFO by design, so a green validator is not "
                 "evidence that the project is documented. The finish line is that a stranger can answer the five "
                 "boot questions from the repository alone."),
    }


def build_parser():
    p = argparse.ArgumentParser(prog="setup.py", description="Resolve, preflight, install and check the context pack.")
    p.add_argument("subcommand", choices=["resolve", "preflight", "install", "markers", "check"])
    p.add_argument("--target", default=".", help="the repository to work on (default: current directory)")
    p.add_argument("--pack", help="path to a context pack checkout")
    p.add_argument("--cache", help="where a fetched pack is cached")
    p.add_argument("--python", help="interpreter used to run the pack's scripts (default: this one)")
    p.add_argument("--components", help="comma-separated component ids for scoped skeletons")
    p.add_argument("--modules", help="optional module packs: research, data, compute")
    p.add_argument("--profile", choices=["shared-tree", "branch-per-agent"], help="coordination profile")
    p.add_argument("--drop-rules", dest="drop_rules", help="rule modules to leave out (protected ones are refused)")
    p.add_argument("--force", action="store_true", help="install over an existing AGENTS.md (get consent first)")
    p.add_argument("--yes", action="store_true", help="actually write; without it install is a dry run")
    p.add_argument("--no-clone", action="store_true", help="never fetch the pack over the network")
    p.add_argument("--baseline", help="check: baseline file to compare against")
    p.add_argument("--write-baseline", dest="write_baseline", help="check: record current findings as the baseline")
    p.add_argument("--json", action="store_true", help="check: ask the validator for JSON too")
    return p


def main() -> int:
    args = build_parser().parse_args()
    handlers = {"resolve": cmd_resolve, "preflight": cmd_preflight, "install": cmd_install,
                "markers": cmd_markers, "check": cmd_check}
    try:
        result = handlers[args.subcommand](args)
    except SystemExit:
        raise
    except Exception as exc:  # an internal error must be loud, never a silent pass
        fail(f"{type(exc).__name__}: {exc}")
    print(json.dumps(result, indent=2))
    return 0 if result.get("ok", False) else 1


if __name__ == "__main__":
    sys.exit(main())
