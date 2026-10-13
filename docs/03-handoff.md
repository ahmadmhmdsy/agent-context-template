# 03 — Handoff (state)

**Contract**
- **Role:** narrative state — where we are.
- **Mutability:** **append-only, newest first.** Never edit or delete a past
  entry. Correct a past entry by writing a new entry that supersedes it.
- **Read when:** session start, before anything else.
- **Update when:** any milestone, incident, decision, or resume point.

**Why append-only:** the value of this file is that it records what was
believed at the time. Editing history destroys exactly that.

---

## Entry format

Copy _templates/handoff-entry.md. Every entry answers:

- **State** — where the project is right now.
- **Did** — what this session actually changed.
- **Verified** — what was checked, with the command and the result.
- **Unverified / open** — what was not checked and what remains.
- **Next** — the single next step.
- **Blockers** — anything gated, and on what.
- **Artifacts** — paths worth opening, as path:line where possible.

## Rotation

The newest entries stay inline, newest first. Older entries move verbatim to
`docs/handoff/archive-2026.md`; rotation never deletes and never rewrites. A new
entry is prepended inside the markers below.

---

<!-- rotate:begin -->
## 2026-10-13T13:10:00+03:00 — Rotation markers and byte caps landed (Task 6)

**State.** The v2 state model now has its rotation markers. The live regions of
`docs/03-handoff.md`, `docs/04-tasks.md` and `docs/08-coordination.md` are
byte-capped, and both archives are seeded empty for `rotate.py` to fill later.

**Did.** Wrapped the live entries, the live task rows and the claim table in the
rotation markers; kept the handoff region <= 8192 B, the tasks region <= 4096 B
and the claims region <= 2048 B; seeded `docs/handoff/archive-2026.md` and
`docs/tasks/archive-2026.md`.

**Verified.** PASS — the step-5 check reports one marker pair per file, every
region at or under its cap, the exact `_templates/task-row.md` header once, and
two archive files.

**Unverified / open.** The rotation script (Task 10) does not exist yet, so no
entry has actually moved. The region caps are checked by hand, not yet by the
validator, until Task 11 lands.

**Next.** Run Task 7: make `docs/05-memory.md` a topic registry with shards.

**Blockers.** none.

**Artifacts.** `docs/03-handoff.md`, `docs/04-tasks.md`, `docs/08-coordination.md`,
`docs/handoff/archive-2026.md`, `docs/tasks/archive-2026.md`.

## 2026-10-13T12:55:00+03:00 — v2 router and pointer adapters merged (Tasks 1-5)

**State.** The pack is being rebuilt in place from v1 to v2 on branch `v2`. The
duplicated two-file entry surface is gone: `AGENTS.md` is a facts-and-pointers
router and the four adapters are pointer-only.

**Did.** Landed Tasks 1-5 of the v2 plan — the schema authority, the rule
registry, the router with its component table, and the four facts-free adapters
(commits 9b8d35c..b7a0dc4).

**Verified.** PASS — `scripts/validate_context.py` reports 0 errors; all four
adapters are <= 1024 B with 0 rule ids and one identical post-H1 body hash.

**Unverified / open.** Phases 2-4 of the plan (state model, tooling, adoption)
are not built; plan tasks 6-18 remain.

**Next.** Build the byte-capped state regions and the rotation markers (Task 6).

**Blockers.** none.

**Artifacts.** `_dev/PLAN-2026-10-13-v2-revision.md`, `AGENTS.md`,
`.superpowers/sdd/progress.md`.

## 2026-01-01T00:00:00+00:00 — Initial template created

**State.** The agent context template was generated as an unused skeleton. No
project-specific content has been added.

**Did.** Created the entry files, the rules modules, the docs tree, and the
artifact forms.

**Verified.** PASS — file set confirmed present; validator run.

**Unverified / open.** Every **ADAPT** marker is unresolved. The command table
and hard constraints are placeholders.

**Next.** Resolve the ADAPT markers in AGENTS.md, then write docs/01-project.md
and docs/02-environment.md.

**Blockers.** none.

**Artifacts.** AGENTS.md, README.md (adoption steps).
<!-- rotate:end -->

Rotated entries: `docs/handoff/archive-2026.md`. Rotation moves; it never deletes.
