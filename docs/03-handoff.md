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

## Size policy

- The newest entries carry full detail.
- When the file grows past roughly 200 entries or becomes slow to scan,
  condense entries older than the most recent N into one summary line each,
  preserving date, title, and outcome. Never delete an entry outright; supersede
  it and note the supersession.

---

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

<!-- Superseded entries stay below. Newest at the top of this file. -->
