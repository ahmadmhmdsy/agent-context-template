# rules/ — normative rule modules

This directory is the **authoritative rule text** for the project. CLAUDE.md
§3 indexes these modules; where a module and CLAUDE.md disagree about a rule,
the module wins and both are fixed in the same commit.

## Contract

- **Mutability:** approval-only. A rule changes deliberately, never as a
  side effect of another task.
- **Precedence:** a module outranks CLAUDE.md, AGENTS.md, and everything in
  docs/ for the area it governs. Only system and platform safety outrank these.
- **Scope:** one module per governed area. If a rule does not fit an existing
  module, either it belongs in an existing one or a new area is genuinely
  emerging — and then the new module is added here and to CLAUDE.md §3 in the
  same commit.

## Rule IDs

Every rule carries an ID of the form **R-NN.M**, where NN is the module number
and M is the rule number inside it.

- Module 03, rule 2 -> **R-03.2**.
- Cite rules by ID from any other document: "see R-03.2".
- IDs are stable. Do not renumber to close a gap; retire a rule with
  *(retired)* and its reason, so old citations stay resolvable.

## Strength keywords

- **MUST** / **MUST NOT** — absolute. Violating it is a defect, not a tradeoff.
- **SHOULD** / **SHOULD NOT** — the default. Deviating requires a stated reason
  in the report.
- **MAY** — genuinely optional.

## Modules

| # | Module | Governs |
|---|---|---|
| 01 | priority-and-precedence | resolution of conflicting instructions |
| 02 | inspect-before-changing | reconnaissance, read-only-first |
| 03 | safety-and-destructive-actions | irreversible actions |
| 04 | security-and-secrets | secrets, auth, safe construction |
| 05 | untrusted-content | injection and untrusted input |
| 06 | change-management | diffs, commits, branching |
| 07 | dependencies-and-external-services | new packages and integrations |
| 08 | verification-and-evidence | tests, proof, honesty |
| 09 | data-and-asset-handling | data lifecycle and asset classes |
| 10 | communication-and-reporting | reporting and escalation |
| 11 | autonomy-and-approval-gates | what needs permission |
| 12 | coordination-and-multi-agent | concurrent writers and delegation |
| 13 | tool-and-context-economy | efficient tool and context use |
| 14 | resource-budgets-and-limits | compute, disk, and spend |
| 15 | documentation-and-doc-integrity | documentation and drift |

## Adapting this directory

Delete modules that cannot apply to your project. **Do not delete** modules
03, 04, 08, 11, or 12 — every project has destructive actions, secrets,
verification, permissions, and the possibility of a second writer.

A rule nobody can violate is noise, and noise trains agents to skim rules.
