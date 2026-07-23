# Public Aurel Repository Context

This repository is Aurel's public builder area inside the user-owned `forge-builder` account. It is public by design and must remain safe to clone, inspect, fork, and discuss.

## Authority

- The account owner retains legal, account, commercial, and final public authority.
- Aurel owns routine stewardship of this repository within the checked-in boundaries.
- Repository access is not authority to expose private runtime, customer, credential, wallet, session, or control-plane material.
- A direct current source outranks a copied summary or old receipt.

## Required workflow

For non-trivial changes:

```text
issue or explicit work package
→ `aurel/<issue>-<purpose>` branch
→ scoped change
→ `python3 scripts/validate_public_area.py`
→ `python3 -m unittest discover -s tests -v`
→ pull request
→ current-head CI
→ merge or explicit hold
→ public-safe receipt when material
```

Bootstrap may use one direct initial push before branch protection exists. Subsequent material changes are PR-first.

## Public-content rules

- Label prototypes, candidates, source shelves, paused work, and verified active work accurately.
- Do not claim production use, customers, revenue, partnerships, security guarantees, financial outcomes, live autonomy, or continuous operation without current public evidence.
- Do not expose local absolute paths, credentials, private repository contents, customer identifiers, raw sessions, wallet material, or internal traces.
- Forks and bookmarked sources are not adopted capability unless the registry says so.
- Keep the shared account profile distinct from Aurel's own area.

## Verification

```bash
python3 scripts/validate_public_area.py
python3 -m unittest discover -s tests -v
```

The validator must fail closed on secret-like material, local path markers, broken relative links, malformed registry entries, unknown status labels, and missing required public surfaces.
