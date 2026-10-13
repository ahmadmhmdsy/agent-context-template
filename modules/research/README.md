# Research records (optional module)

Install with `adopt.py --modules research`. A project that runs no experiments can
skip it: nothing in the base pack links here.

## One record per experiment

Each experiment owns one file in the project's research directory. Record every
field below; when a field truly does not apply, write `none` instead of deleting
the line.

- **id** — stable identifier, never reused.
- **question** — the decision this experiment informs.
- **hypothesis** — a falsifiable prediction.
- **falsified if** — the observation that would prove it wrong.
- **gate** — the threshold that separates pass from fail.
- **setup** — environment, inputs, variants and what stays identical.
- **budget** — the time, compute or cost ceiling.
- **stop condition** — the event that ends the run early.
- **command** — exact text that reproduces the run.
- **result** — measured value plus the artifact holding it.
- **verdict** — one token from the vocabulary below.
- **decision** — what changed because of the result.
- **owner**, **date** — who ran it, and when it closed.

## Verdict vocabulary

    accepted | rejected | partial | inconclusive

- **accepted** — gate passed, and a re-run reproduced it.
- **rejected** — gate failed; the hypothesis is dead.
- **partial** — some gates passed; name the ones that failed.
- **inconclusive** — the run did not measure what it claimed.

## Pre-registration form

Copy this block before running anything. A gate written afterwards is not a gate.

    ## <id> — <title>
    - Question:
    - Hypothesis:
    - Falsified if:
    - Gate:
    - Setup:
    - Budget:
    - Stop condition:
    - Owner:
    - Date:

## Result ledger row

Append one row when the experiment closes, newest last.

| id | question | verdict | measured | artifact | date |
|---|---|---|---|---|---|
| | | | | | |

## Deleting this directory loses nothing

Delete this directory freely. The base pack validates with or without it, and no
other shipped document points into it.

