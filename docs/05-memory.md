# 05 — Memory (lessons and decisions)

**Contract**
- **Role:** durable lessons and settled decisions.
- **Mutability:** the registry is updated in place; the shards it points at are
  append-only. Never delete a lesson — supersede it with a new entry that
  states what changed.
- **Read when:** before touching anything non-obvious.
- **Update when:** a hard-won gotcha, a surprising failure, a settled decision,
  or a reversed assumption.

**Why this file exists:** the same mistake is rediscovered, at full cost, every
time it is not written down. This is the cheapest place to put it.

---

## Topics

This registry lists topics, never individual lessons.

| topic | shard | entries | date range | last updated |
|---|---|---|---|---|
| general | docs/memory/general.md | 2 | 2026-01-01 | 2026-01-01 |
