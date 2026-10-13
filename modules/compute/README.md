# Compute and shared resources (optional module)

Install with `adopt.py --modules compute`. It gives a heavy job the same gate,
read-back and stop discipline on every launch.

## Resource budgets

State the ceiling and the headroom rule per resource, from measurement rather
than assumption.

| Resource | Ceiling | Headroom to leave | Measured how | Last verified |
|---|---|---|---|---|
| | | | | |

## Exclusive resources

List what only one job may hold at a time, and the name that identifies the
holder. A second holder behind an exclusive resource is an incident.

| Resource | Held by | Acquired how | Released how |
|---|---|---|---|
| | | | |

## Launch gate

Before a heavy run, confirm all of these and record the answers:

1. The resource is measured free right now, not assumed free.
2. No exclusive resource is already held by another job.
3. The budget and the stop condition are written down first.
4. The command is recorded exactly as it will run.
5. A checkpoint or resume path exists for a long run.

## Artifact read-back

A run is not finished when the process exits. Read the artifact the run produced,
state the path that holds the result, and compare it with the gate. A success
message from the process is self-reported and does not replace the read-back.

## Stop conditions

Stop and report when any of these holds:

- The budget is spent, whether or not the run looks close.
- The exclusive resource's holder changes mid-run.
- Output stops advancing while the process still lives; inspect progress before
  calling it hung.
- The result file grows past its forecast size.

## Deleting this directory loses nothing

This module owns no numbers by itself; the project declares its own limits in its
environment document, and removing it deletes no configuration.

