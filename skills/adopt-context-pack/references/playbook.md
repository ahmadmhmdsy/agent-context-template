# Adoption playbook

Companion to `SKILL.md`. Read the section you need; the order below is the
order that works.

- Part 1 - reconnaissance, and how to map a project onto the pack
- Part 2 - installing, including multi-component repositories
- Part 3 - reconciling an existing agent system
- Part 4 - clearing inherited state
- Part 5 - the validation loop, and baselines
- Part 6 - failure modes measured by this pack's own adoption runs
- Part 7 - honest reporting

## Part 1 - reconnaissance

The pack asks questions a machine cannot answer, and it asks them in a fixed
order. Answer them in the same order, in one pass, before installing:

1. **Purpose.** One sentence: what, for whom. If two sentences are needed, the
   project has two purposes and the non-goals section is where that gets fixed.
2. **The proof command.** Open the real configuration (`pyproject.toml`,
   `package.json`, `Makefile`, CI workflow) and find the command CI runs.
   Then run it. The command you ran, with the output you saw, is what goes in
   the scoped entry - not the documented one.
3. **Environment.** Runtime, package manager, database, external services,
   hardware. Read each version back from the machine. Anything you could not
   execute is written as unverified, in the row that has a "Verified by" column
   waiting for exactly that admission.
4. **Components.** List the directories that have their own build, test, or
   deployment story. Each one is a scoped `AGENTS.md`; each one must name its
   own smallest validation command. This is the single highest-value mapping in
   the whole adoption, because it is where local knowledge otherwise dies.
5. **Sources of truth.** For every number the project reports (a test count, a
   latency, a score), name the artifact that is authoritative and the command
   that regenerates it. A number that exists only in a chat message is not
   reported, it is remembered.

Useful aliases: a repository whose root is one package has one component; a
repository with `packages/*` or a service + a client has two or more. If you
cannot tell, the entry point's component table is the place to write the
uncertainty down rather than guess a structure.

## Part 2 - installing

```text
setup.py install --target <repo> --components api,worker --modules data --yes
```

The installer is a dry run until `--yes`, and it refuses a target that already
has `AGENTS.md` unless `--force` is given. Three things it will tell you and
you should not suppress:

- the target is not a git repository (nothing can be snapshotted or diffed;
  the pack's rules assume version control);
- the target still contains `ADAPT` markers (expected on a first install, and
  the reason `--allow-placeholders` exists);
- protected rule modules were requested for dropping and refused (they are
  protected because a missing safety rule is not a smaller pack, it is a
  missing safety rule).

Measured on a two-component fixture: a freshly installed target reports
`0 errors, 0 warnings` before a single project fact has been written. The
validator checks shape, not truth - which is exactly why the marker sweep is
the finish line and the validator is a floor.

The plan's own accounting is not evidence that nothing else was touched either:
`setup.py install` reports the target's `git status` before and after for that
reason. Adopt into a clean worktree if the project has one, so the diff is
readable.

## Part 3 - reconciling an existing agent system

Assume the target already has a mature context system (its own `AGENTS.md`,
a rules tree, handoff/memory/task files, maybe generated state). This is the
common case for a serious repository, and it is where a careless adoption does
real damage: the result is two of everything, and no rule saying which wins.

**Decide per file, not per directory, and write the decision down.** For each
collision:

| Situation | Decision |
|---|---|
| the live entry point is richer than the pack's | keep it, and point it at the pack's mechanisms |
| a live file is already a pointer-only adapter | keep it; do not replace it with the pack's copy |
| the live identity file has an owner and a review date | keep it; the pack's is a template of the same idea |
| the live `README.md` is the project overview | keep it; the pack's README describes the pack |
| `.gitignore` differs | merge - append the pack's lines, remove nothing |
| the live rules are a different schema, registered by an index | keep them; adopt the pack's *content* only where the live tree has no equivalent, and use `--drop-rules` for the numbered modules |

Then the structural collisions, which matter more than any single file:

- **Two rule trees.** Two registered rule sets with no precedence rule gives
  every agent two places to look and no way to choose. Either the numbered
  modules become the only tree, or they are dropped and the live tree stays.
  Adopting both is not a compromise, it is an ambiguity.
- **Two doc trees.** The pack's numbered documents can sit beside an existing
  `docs/` tree, but then the entry point must say which one holds which kind
  of truth. Prefer adopting the *mechanisms* - the schema/vocabulary authority,
  handoff, tasks, memory, coordination - over the full set.
- **Scoped entries.** The pack wants a smallest validation command in every
  scoped `AGENTS.md`. If the live tree has eight scoped entries that name
  none, this is a project-wide edit, not an installation step. Land it as its
  own change, component by component.
- **Contract blocks.** The pack wants each `docs/` file to declare a Contract
  (role, mutability, when to read, when to update). A pre-existing docs tree
  will not have them. Do not lower the check; add the blocks over time or
  record the findings in a baseline.

Recommended order, smallest first:

1. purely additive changes only: the `.gitignore` lines, the new mechanism
   documents beside the existing ones;
2. point the existing entry point at the new mechanisms from its read matrix,
   one update trigger at a time;
3. record a baseline so the new mechanisms are protected without demanding a
   mass rewrite;
4. only then decide whether the numbered rule modules replace anything. On the
   evidence of this pack's own adoption audit, usually they should not.

## Part 4 - clearing inherited state

```text
docs/03-handoff.md      inline region (the pack's own entries)
docs/04-tasks.md        Now region (the pack's own task rows)
docs/05-memory.md       plus docs/memory/* shards
docs/handoff/archive-*.md, docs/tasks/archive-*.md
LICENSE                 the pack's copyright line
README.md               the pack's failure table
```

Clearing these is not vandalism: they are the pack's history, they are wrong
for every adopter, and the pack says so itself. What must never be cleared is
anything that records *this* project's work.

Leave the seeded file *structure* (regions, tables, headers) in place - the
validator checks those shapes - and empty only the content.

## Part 5 - the validation loop

```text
setup.py check --target <repo>                 # findings
setup.py check --target <repo> --write-baseline docs/.baseline.json
setup.py check --target <repo> --baseline docs/.baseline.json
```

Work the findings top down: an error means a document is broken or a scoped
entry is missing its proof; a warning means something will rot (a stale date, a
duplicated fact). Fix the document rather than the check.

A baseline is the sanctioned way to live with pre-existing debt: it records
exactly which findings were already there, so the check keeps catching *new*
ones. Two rules for it: re-record it deliberately (a baseline silently
refreshed every run is a check that has been switched off), and give it a
review date.

## Part 6 - failure modes measured by this pack's own adoption runs

These were found by installing the pack into a real project, not by reading it:

- **the marker sweep is not optional.** After adoption, the validator is green
  while 15 files still carry `ADAPT` markers - all INFO. An agent that stops at
  "0 errors, 0 warnings" has left the project undocumented and reported success.
- **a scoped entry without a validation command is an error, and it is right.**
  It caught the pack's own scaffolding, and it catches a component whose proof
  nobody wrote down.
- **the packaged `.gitignore` can be incomplete for the target's toolchain.**
  Running the project's own tests during adoption produced a cache directory
  the ignore list did not cover. Run the tests, then look at `git status`.
- **a form's markers stay.** `_templates/*`, `docs/09-decisions/0000-template.md`
  and `docs/10-runbooks/_template.md` are *supposed* to keep theirs. Counting
  them as gaps wastes a pass over every adoption.
- **the entry point's cap is real.** The boot set has a byte budget; adding a
  paragraph of project prose to `AGENTS.md` is how a router turns into a
  document nobody can afford to read. Project detail belongs in a document the
  router points at.

## Part 7 - honest reporting

End with:

- the outcome, and the declared labels (`PASS`, `FAIL`, `SKIPPED`,
  `BLOCKED`, `NEEDS_USER_DECISION`) - anchored in the pack's own vocabulary,
  not a new one;
- the exact artifacts: files written, the validation command and its output;
- the five questions and which of them still say `unknown`;
- what you did not measure, stated as a limitation rather than smoothed over.

A PASS on the mechanical half and a BLOCKED on the behavioural half are two
results. Averaging them into "done" is the one thing this pack's doctrine
forbids most clearly.
