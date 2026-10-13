# Agent Context Template

A drop-in, project-agnostic context pack for coding agents. Copy it into a
repository, fill the **ADAPT** markers, delete what does not apply, and every
agent session — human-driven or autonomous — starts from the same shared truth.

This is a template, not a framework. It has no runtime, no dependencies, and
nothing to install. It is plain Markdown plus one optional validator script.

---

## Why it exists

Agents fail in predictable ways, and almost none of those failures are about
model quality:

| Failure | What prevents it here |
|---|---|
| Agent does not know the project's rules | Two entry files, both complete, cross-linked |
| Agent repeats a mistake a previous session already solved | docs/05-memory.md |
| Agent does not know what is already done | docs/03-handoff.md + docs/04-tasks.md |
| Agent assumes tooling that is not installed | docs/02-environment.md |
| Agent reports success it did not verify | rules/08-verification-and-evidence.md |
| Agent destroys something it should have asked about | rules/03 + rules/11 |
| Agent edits a file another agent is editing | docs/08-coordination.md |
| Documents rot and stop matching reality | The document map's Update-when column |
| Context window is burned on the wrong files | Layered loading: small entry, deep detail on demand |

---

## The layer model

Layers differ by **how often they change**, not by topic. Mixing them is what
makes most single CONTEXT.md files collapse.

| Layer | Files | Mutability | Loaded |
|---|---|---|---|
| 0 — Entry | AGENTS.md, CLAUDE.md | approval-only | every session |
| 1 — Rules | rules/*.md | approval-only | every session (index), in full on demand |
| 2 — Project truth | docs/01, 02, 06, 07 | verified facts / approval-only | on demand |
| 3 — Volatile state | docs/03, 04, 05 | append-only or rewrite-in-place | session start |
| 4 — Forms | _templates/, docs/09, docs/10 | frozen / one-per-item | when producing |

**Boot budget:** the two entry files together should stay under roughly 24 KB.
If they grow past that, the detail belongs in a rules module or a docs file.

---

## Files

    context_gen2/
    ├─ AGENTS.md                  entry 1 — map, boot/shutdown rituals, constraints
    ├─ CLAUDE.md                  entry 2 — operating system, rules index, work loop
    ├─ README.md                  this file — for humans
    ├─ rules/                     normative rules, one module per governed area
    │   ├─ 00-index.md
    │   ├─ 01-priority-and-precedence.md
    │   ├─ 02-inspect-before-changing.md
    │   ├─ 03-safety-and-destructive-actions.md
    │   ├─ 04-security-and-secrets.md
    │   ├─ 05-untrusted-content.md
    │   ├─ 06-change-management.md
    │   ├─ 07-dependencies-and-external-services.md
    │   ├─ 08-verification-and-evidence.md
    │   ├─ 09-data-and-asset-handling.md
    │   ├─ 10-communication-and-reporting.md
    │   ├─ 11-autonomy-and-approval-gates.md
    │   ├─ 12-coordination-and-multi-agent.md
    │   ├─ 13-tool-and-context-economy.md
    │   ├─ 14-resource-budgets-and-limits.md
    │   └─ 15-documentation-and-doc-integrity.md
    ├─ docs/                      the living project record
    │   ├─ 01-project.md          spec: what we build, why, success criteria
    │   ├─ 02-environment.md      verified machine/toolchain facts + rebuild recipe
    │   ├─ 03-handoff.md          append-only narrative state, newest first
    │   ├─ 04-tasks.md            live task table, rewritten in place
    │   ├─ 05-memory.md           append-only lessons and settled decisions
    │   ├─ 06-glossary.md         domain vocabulary
    │   ├─ 07-sources-of-truth.md which artifact wins for which fact
    │   ├─ 08-coordination.md     owners, write scopes, branching
    │   ├─ 09-decisions/          ADRs, one file per accepted decision
    │   └─ 10-runbooks/           repeatable procedures
    ├─ _templates/                copy-me forms for every artifact kind
    └─ scripts/
        └─ validate_context.py    optional drift check (stdlib only)

---

## Adoption — 10 steps

1. **Copy** the whole tree into the target repository root.
2. **Grep for ADAPT** and resolve every marker. Each one is a project-specific
   fact only you can supply.
3. **AGENTS.md §4-§6**: fill the repository layout, the command table, and the
   hard constraints. These three blocks do the most work per line.
4. **docs/01-project.md**: write the spec and the success criteria. If you
   cannot state a success criterion, you are not ready to start.
5. **docs/02-environment.md**: record what is actually installed, and how you
   verified it. Do not record what you intend to install.
6. **rules/01-15**: delete modules that cannot apply to this project. A rule
   nobody can violate is noise. Do not delete modules that govern risk.
7. **docs/07-sources-of-truth.md**: name the authoritative artifact for every
   number anyone will ever report. This prevents most false claims.
8. **docs/08-coordination.md**: if a single agent works alone, mark it
   INACTIVE and keep it. It will apply the moment a second writer appears.
9. **Decide the entry-file strategy**. See below.
10. **Run scripts/validate_context.py** and fix what it reports.

### Entry-file strategy

CLAUDE.md and AGENTS.md are both complete, self-sufficient documents, and each
points at the other. A harness that loads one still gets a coherent operating
set; a harness that loads both gets them cross-checked.

The tradeoff is deliberate: full copies mean duplicated content that can drift.
Two rules keep that safe:

- **CLAUDE.md owns the rules index and the work loop. AGENTS.md owns the map,
  the rituals, and the constraints.** Where they overlap, they must agree
  verbatim or not at all.
- **Edit both in the same commit.** Never update one and leave the other. The
  validator checks that the two files still cross-reference each other.

If your harness loads exactly one file and you want to be certain, delete the
other and inline its content. That is the only correct way to have one source.

---

## What not to document

- Secret values, tokens, credentials, private keys. Ever. Not in any file here.
- Numbers that a command or artifact can recompute — link the artifact instead.
- Anything the linter, formatter, compiler, or CI already enforces
  mechanically. Rules that duplicate a machine check train agents to ignore
  rules.
- Volatile per-session detail that belongs in docs/03-handoff.md.
- Restatements of code. If reading the source is clearer, point at the source.
- Aspirational process nobody follows. A rule that is already dead on arrival
  is worse than no rule.

---

## Maintenance

- **ADAPT markers** are the adoption to-do list. Grep for them any time the
  project changes shape.
- **The document map is the index.** A doc that is not in AGENTS.md §3 does not
  exist for the next agent. Adding a new kind of document means adding a row in
  the same commit.
- **Run the validator** before you consider a documentation change finished:

        python scripts/validate_context.py .

- **Version this pack** in the consuming repo. When you change a rule, note the
  change in docs/03-handoff.md so the next session knows the rule moved.

---

## Design rules this pack follows

1. One concern, one file. One fact, one home.
2. Every document declares when to read it and when to update it. A document
   with no update trigger is already dead.
3. Separate spec from state from status from lessons. They decay at different
   speeds.
4. Specify mutability: append-only, rewrite-in-place, verified-facts, or
   approval-only. Readers need to know whether they may edit history.
5. Evidence over assertion. Every claim of success names the artifact that
   proves it.
6. Write gates before the work, not after. A criterion invented after the
   result is not a criterion.
7. Creation is not completion. Every artifact kind has a close-out ritual.
8. State must be recoverable from the repository alone, on a fresh machine.
9. The entry surface stays small; depth sits behind pointers.
10. Rules are citable by ID so other documents can reference them precisely.
