---
name: adopt-context-pack
description: Install the versioned agent context pack into a repository - the AGENTS.md entry point, SOUL.md identity, scoped rules, and the handoff / tasks / memory / coordination documents that stop an agent from re-learning a project every session. Use this whenever someone wants an agent to actually know a project: "set up agent context here", "onboard this repo for agents", "add AGENTS.md / CLAUDE.md / SOUL.md", "my agent keeps forgetting how to run the tests", "make this project survive between sessions", "hand work off properly", "install the context template", "I want the same discipline in this repo", "why does my agent redo everything", or an agent session that starts by re-reading the whole tree - even when the user never says "pack" and never names a file. Also use it to reconcile or upgrade a repository that already has its own AGENTS.md, rules tree, or handoff/memory files.
---

# Adopt the context pack into a repository

A repository with no context layer makes every session start from zero: the
agent re-reads the tree, guesses how the tests run, re-derives decisions that
were already made, and forgets why the code is shaped the way it is. The pack
fixes that with one entry point, a small boot set a session reads in order, and
documents whose only job is to hold one kind of truth each.

**Installing is the easy half.** The scripts copy files. The real work is
turning the pack's slots into facts about *this* project, and that is judgement
about the project, not file transfer. A skill that only ran the installer would
leave behind a repository that looks documented and answers nothing.

## The one thing that makes this work

The pack ships with `ADAPT` markers in the slots only an adopter can fill, and
the validator reports them as **INFO, not errors**. So a green validator is not
evidence that the project is documented - it is evidence that the files are
well-formed. A target that was just installed reports 0 errors **before a single
project fact has been written** - that is measured, not assumed - so the marker
sweep, not the validator, is the finish line. The five questions are below.

## What lands in the repository

| Layer | What it is | Editable by |
|---|---|---|
| `SOUL.md` | identity: how this project wants agents to behave | owner, deliberately |
| `AGENTS.md` | the entry point: boot order, precedence, component table, frozen surfaces | rarely |
| `CLAUDE.md`, `GEMINI.md`, `.cursor/rules/pack.mdc`, `.github/copilot-instructions.md` | pointer-only adapters for each agent tool; facts-free, under 1 KB | almost never |
| `rules/NN-*.md` | numbered rule modules with stable ids (`R-12.5`), cited by id | slowly, with evidence |
| `AGENTS.md` per subsystem | the nearest entry wins for that directory | as the subsystem changes |
| `docs/00-07*.md` | schema, project, environment, handoff, tasks, memory, glossary, sources of truth | continuously |
| `docs/08-coordination.md` | the claims table for agents working at the same time | per claim |
| `_templates/`, `docs/09-decisions/`, `docs/10-runbooks/` | forms: filled when used | per use |

## Workflow

Run the helper with any Python 3.11+. It never edits a project document and
never writes without `--yes`:

```text
python <skill-dir>/scripts/setup.py {resolve,preflight,install,markers,check} --target <repo> [...]
```

### 0. Locate the pack

```text
setup.py resolve
```

It checks, in order: `--pack PATH`, `$CONTEXT_PACK_HOME`, the directory the
skill itself sits in (so a clone of the pack repository works with no network),
a cache directory, then a shallow clone of the public repository. If the pack
cannot be found and there is no network, stop and ask the user to clone it -
never improvise a pack, and never write a document from memory of what the pack
contains.

### 1. Preflight, then snapshot

```text
setup.py preflight --target <repo>
```

It reports whether the target already has `AGENTS.md`, `CLAUDE.md`,
`SOUL.md`, a `rules/` or `docs/` tree, or legacy agent files
(`HANDOFF.md`, `MEMORY.md`, `TASKS.md`, `CURRENT_STATE.md`). If anything is
there, the adoption is a **reconciliation**, and the pack's own doctrine says
never destroy user work:

- snapshot first (a branch, e.g. `git switch -c context-pack-adoption`, or a
  copy outside the repo);
- get the owner's explicit consent before `--force`; without it, `adopt.py`
  stops at an existing `AGENTS.md`, and that refusal is a decision point, not
  an obstacle to route around;
- read `references/playbook.md` before writing anything, because two rule
  trees with no precedence rule is worse than one rule tree.

### 2. Reconnaissance - the part only you can do

Install the pack *after* you know enough to fill it. Gather:

- **what the project is, and for whom** - one sentence a stranger could repeat;
- **the smallest command that proves a change is good** (the test or check you
  actually ran in this repository, with its real output, not the command the
  README claims);
- **what is installed and how you verified it** - runtime and tool versions
  read back from the machine, each with the command that produced it;
- **the subsystems** that deserve their own scoped `AGENTS.md` (the pack's
  scope rule is "the nearest entry wins", so this is also the list of places
  where local rules must live);
- **which artifact is authoritative** for each number anyone will report
  (a metric file, a registry, a generated report - never a console log).

Facts you measured and facts the user told you are both allowed, and they are
not the same claim. Keep them apart in `docs/02-environment.md`: it has a
"verified by" column precisely so a guess cannot hide in a version number.

### 3. Install

```text
setup.py install --target <repo> [--components id1,id2] [--modules research,data,compute] [--profile shared-tree|branch-per-agent] [--force] [--yes]
```

Without `--yes` it is a dry run: it prints the exact `adopt.py` command and
writes nothing. Run the dry run, look at the plan, then re-run with `--yes`.
Notes that matter:

- `--components` writes one scoped skeleton per component. A single-package
  repository needs none; a monorepo needs one per package or the local rules
  have nowhere to live.
- `--modules` copies optional packs (`research`, `data`, `compute`); what you
  do not name is not copied.
- `--drop-rules` omits rule modules that cannot apply. The safety, security,
  verification, autonomy, coordination and scope modules are refused by the
  pack - do not try to drop those.
- `--allow-placeholders` is passed for you: a fresh install always still has
  markers, and clearing them is step 5, not a precondition.
- the result also carries the target's own `git status` before and after. Treat
  that as the evidence of what changed, not the plan's arithmetic - a plan that
  says "wrote 60 files" while the tree did not move is a fact worth having.

### 4. Clear the inherited state

The pack ships its own history in its state files. Leave it and the next
session boots into the pack's project and reads it as this one's.

- `docs/03-handoff.md` inline region, `docs/04-tasks.md` Now region,
  `docs/05-memory.md` and `docs/memory/*`, `docs/handoff/archive-*.md`,
  `docs/tasks/archive-*.md`;
- the `LICENSE` copyright line (it carries the pack's, not the project's);
- the failure table in `README.md` - that table is the pack's history, not this
  project's evidence. Rewrite each row once this project has real failures.

Deleting the *pack's* seeded entries is expected and safe. Deleting the
project's own files never is.

### 5. Resolve the markers that remain

```text
setup.py markers --target <repo>
```

It splits them into three kinds, and the difference is the whole point:

- `home` - a fact about this project that nobody has written down yet. Fill it,
  or write `unknown`. An acknowledged unknown is a decision; a deleted section
  is an oversight.
- `seed` - the pack's own history, shipped inside the state files. Clear it in
  step 4; a marker there is not a question about this project. The count should
  drop when you re-run this command.
- `form` - a slot inside a template, filled each time the form is used. Leave
  it.

Work in this order, because each step makes the next one easier:

1. `docs/01-project.md` - purpose, users, scope, non-goals, and success
   criteria that someone who has never seen the project could evaluate. Write
   criteria *before* measuring; a criterion invented after the result is not a
   criterion.
2. `docs/02-environment.md` - what is installed, and how it was verified.
3. `docs/07-sources-of-truth.md` - which artifact wins for each reported number.
4. `AGENTS.md` - the component table (delete the `ADAPT` row and give every
   row a real scoped entry) and the frozen surfaces (the things agents must not
   touch).
5. each scoped `AGENTS.md` - its boundaries, hazards, and its smallest
   validation command. The pack's validator errors on a scoped entry with no
   validation command, which is the check that catches a component whose proof
   nobody wrote down.
6. `docs/06-glossary.md`, `docs/10-runbooks/`, and the rest, as the project
   needs them.

### 6. Reconcile what already existed

If step 1 found an existing agent system, do not run both. Read
`references/playbook.md` §Reconciling. The short version: map the old content
into the pack's homes, keep the old entry point if it is richer than the pack's
and point it at the new mechanisms, adopt the *mechanisms* before the numbered
rules, and record the validator's findings on the pre-existing tree in a
baseline rather than rewriting dozens of files on day one.

### 7. Validate, then report honestly

```text
setup.py check --target <repo>
```

Repeat until it exits 0. Then report:

- which of the five questions below now has a home, and which are still
  `unknown` - deliberately;
- the exact validation command you ran and its real output;
- what you did not measure.

A finding you recorded in a baseline is a decision; a check you weakened to get
to zero is not. Never reword a FAIL or a BLOCKED into a PASS, and never present
unmeasured work as measured.

## Definition of done

The repository is adopted when someone who has never seen it - or the pack -
can answer these five questions from the repository alone:

| # | Question | Home |
|---|---|---|
| 1 | What is this project, and for whom? | `README.md`, `docs/01-project.md` |
| 2 | Where are we now? | `docs/03-handoff.md`, newest entry |
| 3 | What is next? | `docs/04-tasks.md`, Now region |
| 4 | What must an agent never do here? | `AGENTS.md` component table + frozen surfaces, nearest scoped `AGENTS.md` |
| 5 | How is a change proven? | the scoped `AGENTS.md`'s smallest validation command |

Filling a home is not proving a stranger can read it. If you wrote those
answers yourself, your reading them back is not evidence - say so and let the
owner or a fresh session test it.

## Rules that do not bend

- **Never invent a fact.** `unknown` is a valid, honest value; a plausible
  guess in `docs/02-environment.md` costs the next session more than a blank.
- **Never write a secret into the pack.** Scan before you commit; the pack's
  `rules/04-security-and-secrets.md` is the policy.
- **Never `--force` without a snapshot and consent.**
- **Never delete a project document to make a validator happy.** Record it in a
  baseline instead.
- **Never claim a validation you did not run.** Passing on a sample is not
  passing.
- **Keep the pack's doctrine:** no second copy of any fact, adapters stay
  pointers, and the entry point stays inside its byte cap.

## Files

- `scripts/setup.py` - resolve, preflight, install, markers, check. Start here.
- `references/playbook.md` - the full procedure: reconnaissance, component
  mapping, reconciliation with an existing system, the validation loop, and the
  failure modes this pack's own adoption test runs hit.
- `references/pack-reference.md` - the vocabulary the pack will hold you to:
  flags, exit codes, byte caps, check names, rule and citation forms, boot
  order, and the marker inventory.
