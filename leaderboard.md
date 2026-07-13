# AI Money Lab ledger

> Revenue totals include only amounts declared in machine-readable experiment manifests. A value of zero means no verified revenue has been recorded; it does not imply zero cost.

## Current ranking

The project does not rank experiments by storytelling quality. Records are ordered by experiment ID and display status, evidence, and revenue separately.

| ID | Experiment | Status | Revenue | Evidence | Conclusion | Report |
|---|---|---|---:|---|---|---|
| 001 | AI resume optimizer | Inconclusive | CNY 0 | `self-test` | MVP ran locally; acquisition hypothesis untested | [Result](experiments/001-ai-resume-optimizer/result.md) |

## Machine-validated totals

- Experiments: **1**
- Closed: **1**
- Succeeded: **0**
- Failed with sufficient evidence: **0**
- Inconclusive: **1**
- Verified revenue recorded: **CNY 0**

Run `python lab.py summary` to calculate totals from the `experiment.json` files.

## Interpretation

The first record is intentionally not labelled a verified failure. The product self-test and the market-acquisition test are different hypotheses, and only the first was exercised.
