# Contributing

Contributions are welcome when they improve a real public artifact, verifier, documentation contract, or community workflow.

## Before opening a change

1. Search existing issues and pull requests.
2. Link the direct source or reproducible problem.
3. Keep the proposal bounded.
4. Avoid secrets, private data, customer identifiers, wallet material, and local absolute paths.
5. State whether the change is verified, a candidate, staged, planned, paused, or a source-shelf update.

## Local verification

```bash
python3 scripts/validate_public_area.py
python3 -m unittest discover -s tests -v
```

## Pull requests

A useful pull request explains:

- outcome and scope;
- exact files changed;
- commands and actual results;
- claims introduced or removed;
- security and privacy boundary;
- rollback or revert path.

Passing CI is required evidence, not automatic proof that a public claim is true.
