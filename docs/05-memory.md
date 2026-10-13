# 05 — Memory (lessons and decisions)

**Contract**
- **Role:** durable lessons and settled decisions.
- **Mutability:** **append-only.** Never delete a lesson. Supersede it with a
  new entry that states what changed.
- **Read when:** before touching anything non-obvious.
- **Update when:** a hard-won gotcha, a surprising failure, a settled decision,
  or a reversed assumption.

**Why this file exists:** the same mistake is rediscovered, at full cost, every
time it is not written down. This is the cheapest place to put it.

---

## Entry format

One entry per lesson cluster: a dated heading, then one bullet per lesson.

Each bullet MUST contain: the claim in bold, the condition under which it
holds, and the evidence or reasoning that established it.

    ## <date> — <short title>

    - **<the claim, in one sentence.>** <The condition, the evidence, and what
      to do differently.> (<date, source>)

**Rules**
- One lesson per bullet. A bullet with two lessons gets half-followed.
- State the condition. An unconditional lesson becomes wrong the moment the
  environment changes.
- Include the date and the source — a run, a file, a decision by the owner.
- Supersede, never rewrite. If a lesson was wrong, the new entry says so.

---

## 2026-01-01 — Template memory initialized

- **Record a lesson the moment it is learned, not at the end of the session.**
  Session-end memory writes are the ones that get skipped when the session
  ends abruptly, and they are always the most valuable ones. (2026-01-01,
  template creation.)
- **A lesson without its condition becomes a superstition.** "Never do X" is
  usually "never do X while Y holds"; write the Y. (2026-01-01, template
  creation.)
