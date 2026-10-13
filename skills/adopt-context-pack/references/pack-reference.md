# Pack reference (context-pack 2.0.0)

The vocabulary the pack holds an adopter to. Read the part you are about to
touch; everything here is enforced or checked by a script, so treat a
disagreement with this file as a reason to read the script.

## Layout

```text
SOUL.md                  identity (owner-editable)
AGENTS.md                the entry point: boot order, precedence, component table, frozen surfaces
CLAUDE.md GEMINI.md      pointer-only adapters, facts-free, <= 1 KB
.cursor/rules/pack.mdc   .github/copilot-instructions.md   (the other two adapters)
rules/NN-<name>.md       18 numbered modules (00-17), stable rule ids
rules/components/<id>.md component-scoped rule notes
docs/00-schema.md        the single home for ordering rules and vocabularies
docs/01-project.md       what and why
docs/02-environment.md   what is installed, and how it was verified
docs/03-handoff.md       where we are now (inline region, rotated)
docs/04-tasks.md         what is next (Now region, rotated)
docs/05-memory.md        durable lessons (+ docs/memory/ shards)
docs/06-glossary.md      the project's words
docs/07-sources-of-truth.md  which artifact wins for each number
docs/08-coordination.md  the claims table for concurrent agents
docs/09-decisions/       decision records    docs/10-runbooks/   procedures
docs/handoff/archive-*.md  docs/tasks/archive-*.md
_templates/              forms (filled when used)
modules/{research,data,compute}/  optional module packs
VERSION  context-pack.json  CHANGELOG.md  LICENSE  .gitignore
.github/workflows/context.yml  the validator in CI
scripts/                 adopt.py, validate_context.py, rotate.py, claim.py, selftest.py, checks.py
```

## Boot set, in order

1. `SOUL.md`  2. `AGENTS.md`  3. the nearest scoped `AGENTS.md`
4. `docs/08-coordination.md`  5. `docs/03-handoff.md`
6. `docs/04-tasks.md` (Now)  7. `docs/02-environment.md`

## Caps (`scripts/_packmodel.py`)

| Surface | Cap |
|---|---|
| each adapter | 1024 B, and facts-free |
| `AGENTS.md` entry | 2048 B |
| a scoped `AGENTS.md` | 6144 B |
| `docs/03-handoff.md` inline region | 8 KB, >= 3 entries, 2 KB per entry |
| `docs/04-tasks.md` inline region | 4 KB |
| `docs/08-coordination.md` claims region | 2 KB |
| the whole boot set | 36864 B (36 KB) |

The pack walks the tree with `_dev`, `.git`, `.superpowers`, `__pycache__`,
`.venv`, `.locks` and `skills` skipped, and requires 12 files to be present.
Nothing under those names is copied into a target either.

## Rule ids and citations

- A rule is a bold line in a numbered module: `**R-12.5 - <title>.**`
  (em dash), inside `rules/12-coordination-and-multi-agent.md`.
- Cite a rule bare: `R-12.5`. A document section is cited by the file name
  followed by its exact H2 title in double quotes, with the sentence's period
  *outside* the closing quote - the validator recites those titles, so
  punctuation inside the quotes reads as a missing section.
- Rule modules `03` safety, `04` security, `08` verification, `11` autonomy,
  `12` coordination and `16` scope are protected: `--drop-rules` refuses them.

## Adopting (`scripts/adopt.py`)

```text
--target TARGET            must already exist
--components a,b           scoped skeletons; omit for a single-component project
--modules research,data,compute
--profile shared-tree|branch-per-agent
--drop-rules 03,04,...     protected modules are refused
--force                    proceed over an existing AGENTS.md (otherwise a hard stop)
--apply                    write; without it nothing changes
--allow-placeholders       accept a target that still has ADAPT markers
--json                     machine-readable summary (pretty-printed, so parse by braces)
```

## Validating (`scripts/validate_context.py`)

```text
--root ROOT   --json   --baseline PATH   --write-baseline PATH
```

Exit codes: `0` no findings, `1` findings, `2` usage or internal error.
Baseline format: `{"pack_version": "2.0.0", "review_by": "YYYY-MM-DD", "findings": []}`.

Checks, by name: `c00_required`, `c00_index`, `c00_paths`, `c00_contracts`,
`c01_adapter_purity`, `c02_scoped_entries`, `c03_vocabulary`,
`c04_evidence`, `c05_timestamps`, `c06_freshness`, `c07_ordering`,
`c08_archives`, `c09_inline_caps`, `c10_rule_ids`, `c11_duplicate_facts`,
`c12_secrets`, `c13_locks` (plus an INFO-only `c00_adapt` marker count).

What they are looking for, in plain terms: everything the packs requires is
present and reachable; adapters carry no facts and stay under their cap; every
scoped entry names a validation command; the boot set fits its budget; the
ordering tables and vocabularies match `docs/00-schema.md`; every claim of
evidence points at a real path; timestamps and freshness dates are sane; the
archives match their live files; rule ids resolve; no fact is stated twice; no
secret is committed; and a lock is not held by an agent that has gone.

## Concurrency helpers

```text
claim.py acquire|release|status|doctor  --name --owner --ttl --root [--json]   (locks in docs/.locks)
rotate.py [--check] [--apply] [--year YYYY]                                     (dry run by default)
selftest.py                                                                     (the pack's own suite)
```

## Serialized table orders (do not reorder columns)

| Table | Columns |
|---|---|
| claims | `| task | owner | scope | claimed_at | expires_at | state |` |
| tasks | `id | title | status | owner | scope | gate | evidence` |
| toolchain | `| Tool | Version | Verified by | Notes |` |

## ADAPT markers

Two kinds, and the difference decides whether you must act:

- **home** - a fact about the project. Measured on 2.0.0: 8 files, ~51 markers,
  led by `docs/02-environment.md` (~22), `docs/01-project.md` (~17) and
  `docs/07-sources-of-truth.md` (~5), plus `AGENTS.md` (~2).
- **form** - a slot inside a template, filled when the form is used:
  `_templates/*`, `docs/09-decisions/0000-template.md`,
  `docs/10-runbooks/_template.md`. Measured on 2.0.0: 6 files, ~46 markers.

The validator reports every marker as INFO, never as an error, so a green run
does not mean the project is documented. `setup.py markers` classifies the two
kinds for you.

## Environment

Python 3.11+. Standard library only - no third-party dependency, by design, so
an adoption cannot fail because a lockfile went stale.
