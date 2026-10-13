# 06 — Glossary (domain language)

**Contract**
- **Role:** the canonical meaning of project-specific terms.
- **Mutability:** append-only. Redefining a term requires a new row and a note
  on the old one.
- **Read when:** a domain term is unclear, or before naming anything new.
- **Update when:** a term is coined, imported, or redefined.

**Why this file exists:** agents confidently misuse domain vocabulary, and
every downstream artifact inherits the misuse. One table prevents it.

---

| Term | Meaning here | Not to be confused with | Source |
|---|---|---|---|
| **ADAPT** | | | |
| task | a tracked unit of work with an ID, a status, and an owner | a to-do note | docs/04-tasks.md |
| agent | an autonomous or semi-autonomous worker operating in this repository | a process or service | AGENTS.md |
| durable | survives the session because it is written to a file in this repository | cached, in memory | rules/15 |

## Rules

- **Canonical spelling.** One spelling per term; list variants as "also seen
  as". Inconsistent spelling breaks search.
- **Define by use, not by dictionary.** What does it mean *in this project*?
- **Name the near-miss.** The most useful column is what the term is commonly
  confused with.
- **Add the term the first time it is used ambiguously** — that is when the
  cost of not defining it is visible.
