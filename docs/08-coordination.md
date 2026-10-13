# 08 — Coordination

**Contract**
- **Role:** who may write what, and how concurrent work is serialized.
- **Mutability:** approval-only.
- **Read when:** before any work that shares files or resources with another
  writer.
- **Update when:** owners, write scopes, branching, or shared resources change.

Full protocol: rules/12-coordination-and-multi-agent.md.

---

## Mode

**ADAPT** — declare one, and keep it accurate:

- **ACTIVE — multi-writer.** More than one writer may operate concurrently.
  Every task declares an owner and a write scope before editing.
- **INACTIVE — single writer.** Exactly one writer at a time. The rules below
  still apply the moment a second writer appears; marking this section inactive
  is a statement about the present, not a permanent exemption.

**Changing the mode requires the owner's decision** and a row in the mode
history below.

## Mode history

| Date | Mode | Reason | Decided by |
|---|---|---|---|
| | INACTIVE | initial template state | — |

## Owners

| Owner | Role | Owned paths | May approve |
|---|---|---|---|
| **ADAPT** | | | |

## Write-scope conventions

- A scope is a file or a directory prefix, declared before editing.
- **Overlapping scopes are serialized, not raced.** The second writer waits or
  takes a handoff.
- Shared files with many writers — this file, docs/04-tasks.md — are edited in
  small, short-lived changes.
- On a rejected write, re-read the current content, reapply the intent onto it,
  and retry. Never overwrite with a stale copy.

## Active claims

| Task | Owner | Scope | Started |
|---|---|---|---|
| — | — | — | — |

## Branching

**ADAPT** — branch strategy, naming, who merges, what must never be pushed
directly to the main branch.

## Shared and exclusive resources

| Resource | Exclusive? | Serialization rule |
|---|---|---|
| **ADAPT** | | |

## Handoff protocol

When work passes between writers: update docs/03-handoff.md, update the task
row's owner and status, and state explicitly what is finished, what is
half-done, and what must not be touched.

## Escalation

**ADAPT** — who resolves a disagreement between writers, and how quickly.

## Conflict resolution

1. Stop both writers on the contested artifact.
2. Record both positions with evidence in docs/05-memory.md.
3. Escalate to the owner named above.
4. Apply the decision; do not re-litigate it in the file.
