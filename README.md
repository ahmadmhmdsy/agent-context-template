# Agent Context Template

A drop-in, project-agnostic context pack for coding agents. Copy it into a
repository, fill the **ADAPT** markers, delete what does not apply, and every
agent session — human-driven or autonomous — starts from the same shared truth.

Version 2.0.0. This is a template, not a framework: no runtime, no dependency,
nothing to install. It is plain Markdown plus a few Python 3.11+ scripts from
the standard library that change nothing unless you run them.

---

## What this is

One written entry, [AGENTS.md](AGENTS.md), states the repository's stable policy
and routes every other question to the file that owns the answer. Nothing else
restates it. Harnesses that insist on their own filename get a pointer-only
adapter under 1 KB that says where to go.

Layers differ by **mutability, not topic**, because mixing mutability is what
makes a single all-purpose context file collapse:

| Layer | Files | Mutability |
|---|---|---|
| Entry | `AGENTS.md`, and one adapter per harness | approval-only, and the adapters say nothing |
| Rules | `rules/*.md` | approval-only; read in full on demand |
| Project truth | `docs/01`, `02`, `06`, `07` | verified facts, each with a review date |
| Volatile state | `docs/03`, `04`, `05`, `08` | append-only or rewritten in place, capped, rotated |
| Forms | `_templates/`, `docs/09`, `docs/10` | frozen, one file per item |

Markdown in the repository is the record. There is no generated snapshot to
regenerate, no second copy of any fact, and no renderer.

---

## The boot set

Every session reads these, in this order, and nothing else is required to start:

1. `SOUL.md` — identity, the same in every project.
2. `AGENTS.md` — the router.
3. the nearest scoped `AGENTS.md` above the working directory, when one exists.
4. `docs/08-coordination.md` — the active claims.
5. `docs/03-handoff.md` — the newest entry.
6. `docs/04-tasks.md` — the Now section.
7. `docs/02-environment.md` — when you are going to run anything.

The set is budgeted, and the validator fails when a part exceeds its cap:

| Component | Cap |
|---|---|
| `SOUL.md` | 4 KB |
| `AGENTS.md` | 12 KB |
| nearest scoped `AGENTS.md` | 6 KB |
| `docs/03-handoff.md` inline region | 8 KB, at least 3 entries, 2 KB per entry |
| `docs/04-tasks.md` inline region | 4 KB |
| `docs/08-coordination.md` claims region | 2 KB |
| **Whole boot set** | **≤ 36 KB** |
| each adapter | 1 KB, and facts-free |

---

## Adopting it

The pack installs itself. Run it from the pack directory; it is a dry run until
you pass `--apply`, and the flags below are the complete set:

```text
python scripts/adopt.py --target TARGET [--components COMPONENTS]
                        [--modules MODULES]
                        [--profile {shared-tree,branch-per-agent}]
                        [--drop-rules DROP_RULES] [--force] [--apply]
                        [--allow-placeholders] [--json]
```

- `--target` — the repository to install into. It must already exist.
- `--components` — the component ids to write a scoped skeleton for, comma
  separated. Omit it for a single-component project.
- `--modules` — the optional module packs to copy: `research`, `data`,
  `compute`. Anything you do not name is not copied.
- `--profile` — `shared-tree` (the default) or `branch-per-agent`, which
  changes the coordination text the target receives.
- `--drop-rules` — rule modules to leave out, for rules that cannot apply to
  the project. The protected modules (`03` safety, `04` security, `08`
  verification, `11` autonomy, `12` coordination, `16` scope) are refused.
- `--force` — proceed when the target already has an `AGENTS.md`, which is
  otherwise a hard stop.
- `--apply` — write. Without it nothing changes.
- `--allow-placeholders` — accept a target that still contains **ADAPT**
  markers.
- `--json` — machine-readable summary of what was written, edited and skipped.

Then finish the job by hand, because the pack cannot know your project:

1. **Grep for `ADAPT`** and resolve every marker. Each is a fact only you can
   supply.
2. **Fill the project documents**: `docs/01-project.md` (what and why, with
   success criteria you can actually test), `docs/02-environment.md` (what is
   installed and how you verified it), `docs/07-sources-of-truth.md` (which
   artifact wins for each number anyone will report).
3. **Delete the rules that cannot apply**, and keep every rule that governs
   risk. A rule nobody can violate is noise; a missing safety rule is not.
4. **Clear the state you inherited** — see the next section.
5. **Run the validator** and fix what it reports.

---

## What adoption does and does not guarantee

The scripts copy files and seed state. They do **not**:

- lock anything across machines, or between agents on one machine, unless you
  adopt the optional `scripts/claim.py`;
- preempt or stop a running agent;
- protect you from an agent that ignores the claims table;
- merge two agents' work automatically, or resolve a conflict;
- keep a document true. The pack makes rot visible; it does not prevent it.

The pack coordinates. It enforces only what a script can check.

Two things ship as-is and are yours to change. The `LICENSE` carries this
pack's copyright line — an adopter replaces it with their own. And the failure
table below is this pack's, not your project's: rewrite each row with your own
evidence once you have some.

---

## The state you inherit and must clear

**This is not optional.** The pack ships its own history in its state files, and
an adopter who leaves it there boots into someone else's project and reads it as
their own.

Before first use, clear the three inline regions and both archives:

| Clear | What it holds when it ships |
|---|---|
| `docs/03-handoff.md` inline region | entries describing this pack's own rebuild |
| `docs/04-tasks.md` inline region | this pack's own task rows |
| `docs/08-coordination.md` claims region | claims of this pack's rebuild |
| `docs/handoff/archive-2026.md` | archived handoff entries from this pack |
| `docs/tasks/archive-2026.md` | archived task rows from this pack |

Leave the markers in place. Rotation writes between them, and an empty region
between intact markers is a correct starting state.

The rule that a handoff keeps at least three entries describes what rotation
preserves in a project **in use**; it is not a requirement on a fresh copy. An
empty handoff right after adoption is correct, not a violation.

---

## Validating

```text
python scripts/validate_context.py --root .     # 0 clean, 1 findings, 2 usage
python scripts/validate_context.py --root . --json
python scripts/validate_context.py --root . --baseline _dev/baseline.json
python scripts/rotate.py --root . --check       # dry run; --apply to move
python scripts/selftest.py                      # the scripts' own tests
```

Record a baseline when you adopt a pack into a repository that already has
findings; a baselined finding is reported as such rather than as new. A warning
is informational and never fails the run.

`.github/workflows/context.yml` runs the same three checks in CI. It is
optional and deletable: the pack must lint by hand if you remove it.

---

## Where the failures are caught

Agents fail in predictable ways, and almost none of those failures are about
model quality. Each row says what this pack does about it, and whether that is
**measured** or still **design intent**.

Measured means the mechanism exists and is enforced by a command whose output is
in this repository — not that the pack has been shown to change an agent's
behaviour. Behaviour is measured in the adoption stages described in the design
record, and any row not exercised by a real target stays labelled design intent.

| Failure | What this pack does about it | Status |
|---|---|---|
| Agent does not know the project's rules | one written entry, and adapters that only point at it | measured: the validator checks each adapter is ≤ 1 KB, points at `AGENTS.md`, and states no rule ID |
| Agent repeats a settled mistake | `docs/05-memory.md` as the topic registry, with full lessons in `docs/memory/<topic>.md` | design intent, not yet measured; the row shape is fixed by `docs/00-schema.md` |
| Agent does not know what is already done | the handoff and task regions, capped and rotated | measured: `rotate.py --check` exits 0 and the validator enforces both caps |
| Agent assumes tooling that is not installed | `docs/02-environment.md`, with `Last verified` on each fact | design intent, not yet measured; the validator marks a stale fact, but reading it is the agent's job |
| Agent reports success it did not verify | `rules/08-verification-and-evidence.md`, and evidence that must resolve | measured: the validator resolves the evidence path of every `done` row |
| Agent destroys something it should have asked about | the gates in `rules/03` and `rules/11` | design intent, not yet measured; no check can see intent, only text |
| Agent edits a file another agent is editing | the claims table, and the optional `scripts/claim.py` lock | design intent, not yet measured: the pack coordinates, it does not enforce |
| Documents rot and stop matching reality | every document declares when to read and when to update it | measured in part: `validate_context.py` reports zero errors on this pack; the mapping is checked, the writing is not |
| The context window is spent on the wrong files | the layered map and the 36 KB boot ceiling | measured: the validator fails a boot set over its budget |

---

## What not to document

- Secret values, tokens, credentials, private keys. Ever. Not in any file here.
- Numbers that a command or artifact can recompute — link the artifact instead.
- Anything a linter, formatter, compiler, or CI already enforces mechanically.
  Rules that duplicate a machine check train agents to ignore rules.
- Volatile per-session detail that belongs in `docs/03-handoff.md`.
- Restatements of code. If reading the source is clearer, point at the source.
- Aspirational process nobody follows. A rule that is dead on arrival is worse
  than no rule.

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
6. Creation is not completion. Every artifact kind has a close-out ritual.
7. State must be recoverable from the repository alone, on a fresh machine.
8. The entry surface stays small; depth sits behind pointers.
9. Rules are citable by ID, so other documents can reference them precisely.
