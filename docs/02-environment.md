# 02 — Environment

**Contract**
- **Role:** verified facts about the machine and toolchain.
- **Mutability:** verified facts. Record what is, never what you intend.
- **Read when:** before running anything.
- **Update when:** any machine, toolchain, version, credential location, or
  service change.

**Rule:** every fact here MUST state how it was verified and when. A guessed
version is worse than a missing one, because it is trusted.

---

## How to verify

**ADAPT** — the commands that re-derive the facts below.

    # environment / version sweep — ADAPT
    # package manager + lockfile — ADAPT
    # installed services + ports — ADAPT
    # free disk — ADAPT

## Machine

| Fact | Value | Verified by | Last verified |
|---|---|---|---|
| Operating system | **ADAPT** | **ADAPT** | |
| Architecture | **ADAPT** | | |
| CPU / cores | **ADAPT** | | |
| Memory | **ADAPT** | | |
| Disk (free / total) | **ADAPT** | | |
| GPU / accelerator | **ADAPT** | | |

## Toolchain

| Tool | Version | Verified by | Notes |
|---|---|---|---|
| **ADAPT** runtime | | | |
| **ADAPT** package manager | | | lockfile kind: |
| Build tool | | | |
| Test runner | | | |

## Services and ports

| Service | Where | Port | Started by |
|---|---|---|---|
| **ADAPT** | | | |

## Credentials

Never record values here. Record only the **name**, the **location**, and the
**scope** required.

| Variable | Required for | Where it lives | Committed? |
|---|---|---|---|
| **ADAPT** | | environment / secret store | no |

## Network and access

**ADAPT** — VPN, proxies, allowlists, offline behavior, any endpoint that must
be reachable.

## Capabilities and limits

- **Can:** **ADAPT**
- **Cannot:** **ADAPT**
- **Workarounds in use:** **ADAPT** — and why each is a fallback, not a fix.

## Rebuild recipe

**ADAPT** — the exact sequence to rebuild this environment from nothing. This
is what makes the project recoverable after a machine loss.

    # 1. install runtime
    # 2. install dependencies from the lockfile
    # 3. configure environment variables
    # 4. verify with:
    #    ADAPT

## Known environmental hazards

**ADAPT** — version drift, throttling, shared resources, commands that hang,
anything that has caused a failure before.

## Verification log

Append-only.

| Date | What was verified | How | Result |
|---|---|---|---|
| | initial template created | — | pending |
