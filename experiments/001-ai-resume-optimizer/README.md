# Experiment 001 - AI resume optimizer

This folder preserves the MVP and the final experiment record.

- [Result and limitations](result.md)
- [Machine-readable manifest](experiment.json)
- `app.py`: local Flask MVP retained for reproducibility
- `lean_canvas.md`: original hypothesis notes

The final status is **inconclusive**. The MVP was exercised by the author, but the planned GitHub-only acquisition channel was not tested with external traffic, so there is no defensible market-demand conclusion.

## Run the historical MVP

The MVP has optional third-party dependencies and an optional model API key. It is not required for validating the lab ledger.

```bash
python -m pip install flask requests
python app.py
```

Review the code before providing any API credential. Do not upload real resumes or personal information to public issues or fixtures.
