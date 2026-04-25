# Contributing to RM Orbit

## Pre-Flight Gates (Required)

From repo root:

```bash
./runtime-matrix-gate.sh
./contract-gate.sh
./smoke-gate.sh
```

If a gate fails, resolve drift/contract/runtime issues before opening a PR.

## Recommended Full Validation

```bash
cd Atlas/backend && python3 -m unittest discover -s tests -p "test_*.py"
cd "../../Control Center/server" && npm run test:tenant
cd ../../Calendar/server && npm run test:tenant
cd ../../Planet/backend && python3 -m unittest discover -s tests -p "test_*.py"
cd ../../Mail/backend && PYTHONPATH=. pytest tests/test_eventbus_contract.py
cd ../../Connect/server && npm run test:tenant
cd ../../Meet/server && npm run test:tenant
```

## Pull Requests

Use the repository PR template and include:

- exact gate commands run
- key outputs/pass status
- runtime profile impact (`start-all.sh` vs PM2) when relevant
- doc updates for behavior/port changes

## Runtime Contract

- `PORTS.md` is the canonical registry.
- Keep `start-all.sh` and `ecosystem.config.cjs` aligned with documented profiles.
- `runtime-matrix-gate.sh` enforces this consistency.
