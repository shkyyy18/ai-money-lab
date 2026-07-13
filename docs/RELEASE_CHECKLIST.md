# Release checklist

- [ ] `python lab.py validate` passes.
- [ ] `python lab.py summary` matches README and leaderboard counters.
- [ ] `python -m unittest discover -s tests -v` passes.
- [ ] `python -m compileall -q lab.py tests` passes.
- [ ] Closed experiments include dates, conclusion, evidence level, and a report.
- [ ] Non-zero revenue has privacy-safe `verified-revenue` evidence.
- [ ] No customer data, credentials, resumes, payment IDs, or fabricated proof are staged.
- [ ] GitHub Actions passes and the release tag matches the changelog.
