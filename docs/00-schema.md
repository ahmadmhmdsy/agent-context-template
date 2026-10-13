# 00 — Schema: vocabulary and record fields

The single authority for every controlled value and record field the pack uses.

**Contract**
- **Role:** vocabulary and record-field authority — the one list of legal values
  and field names.
- **Mutability:** approval-only. Adding or changing a value or a field is the
  owner's decision, never an agent's convenience.
- **Read when:** before writing any task, plan, decision, lesson, claim, handoff
  entry or other record.
- **Update when:** the owner adopts a value or a field. Update every document
  that uses it in the same change; a document that uses an unlisted value is
  wrong.

## Vocabularies

| Kind | Values |
|---|---|
| Task status | `pending \| in_progress \| blocked \| done` |
| Report label | `PASS \| FAIL \| SKIPPED \| BLOCKED \| NEEDS_USER_DECISION` |
| Plan status | `draft \| approved \| in_progress \| done \| abandoned` |
| Decision status | `proposed \| accepted \| superseded \| rejected` |
| Rule status | `draft \| active \| superseded \| retired` |
| Lesson status | `observed \| candidate \| validated \| promoted \| rejected` |

Ordering conventions are also declared here so no document can contradict them: handoff newest-first, decisions newest-first, memory shards oldest-first, memory topic registry newest-updated first, tasks rewrite-in-place, contract blocks frozen.

## Record fields

| Record | Fields | Authority |
|---|---|---|
| Verified fact | `Last verified`, `Verified by` | spec §5.3 |
| Memory topic registry row | `topic`, `shard`, `entries`, `date range`, `last updated` | spec §5.2 |
| Handoff entry | heading `## <ISO-8601 with offset> — <title>`; `State`, `Did`, `Verified`, `Unverified / open`, `Next`, `Blockers`, `Artifacts` | `_templates/handoff-entry.md`; spec §5.1, §6.7 |
| Task row | `id`, `title`, `status`, `owner`, `scope`, `gate`, `evidence` | `_templates/task-row.md`; spec §7.2 check 4 |
| Claim | `task`, `owner`, `scope`, `claimed_at`, `expires_at`, `state` | spec §6.5 |
| Lesson | heading `## <date> — <title>`; `Status`, `Lesson`, `Evidence` — the condition and the source belong inside the `Lesson` value | `_templates/lesson.md`; spec §5.6 |
| Decision | heading `# NNNN — <title>`; `Status`, `Date`, `Decided by`, `Supersedes` | `docs/09-decisions/0000-template.md`; spec §5.5 |

This file is the single authority. A document that uses a value not listed here is wrong, even if this file is the one that is stale.
