# AI Money Lab methodology

## 1. Start with a falsifiable question

An experiment must state a defined customer, problem, offer, price, acquisition channel, primary metric, time or spend boundary, and stop rule. "Build an AI app and see what happens" is not an experiment.

## 2. Separate product proof from market proof

- A local self-test can prove that software executes.
- Public traffic can test whether a channel reaches relevant people.
- Conversion can test whether the offer produces a stated action.
- Verified payment can test willingness to pay.

Evidence from one layer must not be presented as proof of a later layer.

## 3. Evidence levels

| Level | Required evidence |
|---|---|
| `none` | No execution evidence. |
| `self-test` | Reproducible local test or sanitized execution record. |
| `public-metrics` | Public or redacted channel and conversion metrics with dates and definitions. |
| `verified-revenue` | Privacy-safe payment evidence tied to the experiment period and currency. |

Narrative confidence never upgrades the evidence level.

## 4. Status definitions

- `planned`: the experiment has not started.
- `running`: the channel test is active and the stop rule has not been reached.
- `succeeded`: the predeclared success rule was met with suitable evidence.
- `failed`: the predeclared failure rule was met with suitable evidence.
- `inconclusive`: execution ended without enough evidence to classify success or failure.

A working MVP with no external traffic is normally inconclusive, not succeeded or failed.

## 5. Revenue rules

Revenue is recorded in the manifest currency. Non-zero revenue requires `verified-revenue` evidence before it can be promoted in the public total. Refunds, taxes, fees, and costs must be explained in the report when relevant. Unknown cost is written as unknown, not zero.

## 6. Privacy and security

Reports must redact names, email addresses, account identifiers, tokens, API keys, payment IDs, resumes, and customer documents. Synthetic fixtures are preferred. Public issues and pull requests must never contain private customer material.

## 7. Stop rules

A stop rule should be observable and bounded, for example:

- stop after 200 relevant landing-page visits if fewer than 3 qualified requests are received;
- stop after CNY 500 in declared acquisition spend;
- stop after 14 days if the stated channel cannot produce measurable traffic.

If the rule changes, record the original rule, the change date, and the reason.

## 8. Required experiment files

Each experiment folder contains:

```text
experiment.json   machine-readable status, dates, revenue and evidence level
result.md          outcome, observed evidence, missing evidence and conclusion
```

Supporting MVP code or evidence notes may be included when they are safe and licensed.

## 9. Validation

Run:

```bash
python lab.py validate
python lab.py summary
```

CI rejects missing fields, duplicate IDs, invalid dates or statuses, negative revenue, invalid evidence levels, and missing reports. Human review remains responsible for deciding whether attached evidence supports the claim.
