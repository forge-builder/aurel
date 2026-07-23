# Receipt: Aurel public-area bootstrap

- Date: 2026-07-23
- Work package: [#1](https://github.com/forge-builder/aurel/issues/1)
- Target: [forge-builder/aurel](https://github.com/forge-builder/aurel)
- Visibility: public
- Bootstrap commit: `3f100c36507e9d1c19888cd9cb806bd04f302383`

## Prior state

The shared `forge-builder` account had Aurel-prefixed forks and a private Studio control plane, but no owned public Aurel home with an explicit identity, project registry, community contract, public boundaries, or verifier.

## Change

Created the public `forge-builder/aurel` repository with:

- an explicit Aurel identity and human-ownership boundary;
- a curated project and contribution map;
- machine-readable status registry;
- public-content, contribution, community, and security contracts;
- issue forms and pull-request template;
- a standard-library validator and six fail-closed tests;
- pinned GitHub-owned checkout action;
- Discussions and Issues enabled;
- private vulnerability reporting enabled;
- secret scanning and push protection active;
- squash-only merges and automatic branch deletion;
- public topics for discoverability.

## Local verification before publication

```text
python3 scripts/validate_public_area.py
→ AUREL_PUBLIC_VALIDATION=PASS
→ files_checked=16
→ registry_entries=8
→ secret and local-path scan passed
→ relative links passed

python3 -m unittest discover -s tests -v
→ 6 tests passed

python3 -m py_compile scripts/validate_public_area.py tests/test_public_area.py
→ exit 0

git diff --cached --check
→ exit 0
```

## Remote verification

- Bootstrap push: `3f100c36507e9d1c19888cd9cb806bd04f302383` on `main`.
- Current-head Actions run: [30047975790](https://github.com/forge-builder/aurel/actions/runs/30047975790) — success.
- Repository API readback: public, Issues enabled, Discussions enabled.
- Private vulnerability reporting API: enabled.
- Secret scanning and secret-scanning push protection: enabled.
- Topics readback: `agentic-systems`, `ai-agents`, `aurel`, `developer-tools`, `human-agent-collaboration`, `open-source`.
- `main` protection readback:
  - pull request required;
  - strict current-head `validate` required;
  - linear history required;
  - resolved conversations required;
  - force pushes disabled;
  - branch deletion disabled;
  - zero mandatory human approvals, so the owner can operate without self-review deadlock.

## Authority and limits

The initial bootstrap used the authenticated human-account credential because the scoped Aurel GitHub App did not yet exist. The repository and this receipt do not authorize exposing secrets, private runtime state, customer material, wallet authority, or private control-plane evidence.

The broad human credential remains a temporary bootstrap path. It must not be described as retired until the selected-repository App completes a live read, issue, branch, draft-PR, and current-head CI smoke suite.

## Deliberately not done

- No account display name, bio, avatar, hireable flag, pin, or Pages deployment changed.
- The shared profile draft was not merged.
- No GitHub App, installation token, private key, or OAuth authorization was created in this bootstrap.
- No private repository, customer body, runtime state, or wallet data was copied here.
- No portfolio candidate was promoted to maintained status.

## Rollback

If the public area is no longer wanted, first close active work, preserve public issue/PR references, and archive the repository. Deletion is not the routine rollback because it would destroy public audit history. Individual bootstrap changes can be reverted through a protected-branch pull request.
