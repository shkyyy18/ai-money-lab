# Contributing

Small, reviewable contributions are welcome.

## Useful contribution paths

- Nominate a bounded experiment through the issue template.
- Improve the manifest validator or tests.
- Review a report for contradictions or unsupported evidence claims.
- Add a privacy-safe evidence pattern or documentation example.

Every experiment needs an `experiment.json` manifest and a human-readable `result.md`. Open an issue before adding an experiment so the customer, channel, metric, stop rule, evidence plan, and privacy boundary can be reviewed first.

Do not submit fabricated revenue, traffic, screenshots, testimonials, private customer material, credentials, copied resumes, or AI-generated proof.

```bash
python lab.py validate
python lab.py summary
python -m unittest discover -s tests -v
python -m compileall -q lab.py tests
```

By contributing, you agree that your contribution is licensed under the repository's MIT License.
