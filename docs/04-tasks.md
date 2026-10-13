# 04 — Tasks (live status)

**Contract**
- **Role:** the current truth about what is being worked on.
- **Mutability:** **rewritten in place.** This is the one document where editing
  history is correct — the table always shows the present.
- **Read when:** session start.
- **Update when:** a task starts, finishes, changes owner, or becomes gated.

**Statuses:** pending | in_progress | blocked | done.
**Blocked always names its gate.** A task waiting on a user decision is blocked,
not in_progress.

---

## Columns

| Column | Meaning |
|---|---|
| ID | stable identifier; never reused |
| Task | what it delivers, in one line |
| Status | pending / in_progress / blocked / done |
| Owner | who is accountable right now |
| Write scope | the paths this task may modify — required when more than one writer is active |
| Gate / next action | what unblocks it, or the immediate next step |
| Evidence | the artifact that proves the status — required for done |

**Evidence rule:** a row marked done with an empty Evidence cell is not done.
Cite the command, file, or run that proves it.

**Pre-registration rule:** write the acceptance criterion before starting work
that is expensive or hard to reverse. A criterion invented afterwards is not a
criterion.

## Now

Only `Now` and `Blocked` rows stay inline. Completed rows move verbatim to
`docs/tasks/archive-2026.md`; rotation moves, it never deletes. The column order
is fixed by `_templates/task-row.md`, so a row can be copied from that form.

<!-- rotate:begin -->
| id | title | status | owner | scope | gate | evidence |
|---|---|---|---|---|---|---|
| T-001 | Resolve all ADAPT markers across the template | pending | — | AGENTS.md, docs/** | start with AGENTS.md §4-§6 | — |
| T-002 | Write the project specification | pending | — | docs/01-project.md | needs owner input | — |
<!-- rotate:end -->

## Blocked

None. A blocked row stays in the live table above with `status: blocked` and a
`gate` that names what unblocks it.
