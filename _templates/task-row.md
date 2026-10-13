| ID | Task | Status | Owner | Write scope | Gate / next action | Evidence |
|---|---|---|---|---|---|---|
| T-NNN | <one-line deliverable> | pending | <owner> | <paths> | <what unblocks it> | <artifact> |

<!--
Fill rules:
- Status is one of: pending | in_progress | blocked | done.
- blocked MUST name its gate in the Gate column. A task waiting on a user
  decision is blocked, not in_progress.
- Write scope is required whenever more than one writer is active. It is the
  file or directory prefix this task may modify.
- Evidence is required for done. It is the command, file, or run that proves
  the status, cited as a path. A done row with an empty Evidence cell is not
  done.
- ID format: T-NNN, stable, never reused.
- Pre-register the acceptance criterion in the Task or Gate cell before
  starting work that is expensive or hard to reverse.
-->
