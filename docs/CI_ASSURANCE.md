# CI assurance contract

This repository uses `.github/workflows/assurance.yml` as a research-safety
and packaging gate.

## Change-time gates

Pushes to `main`, pull requests, merge-queue checks, and manual dispatches run:

- Python 3.11 and 3.12 invariant tests.
- `ResourceWarning` escalation to failure.
- Source/test/script compilation.
- DAEDALUS static scientific audit.
- Coverage measurement with the current non-regression floor.
- Wheel/sdist build and installed CLI smoke test.
- `pip check` after editable and wheel installation.
- A final aggregate gate.

The workflow never runs the authoritative corpus automatically and never spends
protected holdouts merely because CI fired. It does not authorize production or
live execution.

## Scheduled drift gate

The daily schedule is intentionally a single Python 3.12 job to reduce Actions
consumption. It rechecks compilation, the complete test suite, static audit,
dependency consistency, and CLI availability.

## Machine-readable evidence

Every aggregate gate writes `assurance/assurance-summary.json` and uploads it
as a 30-day workflow artifact. It records gate state, commit identity, run
identity, authority, and final result so owner automation or the ICARUS UI can
consume assurance state without reading human logs.

DAEDALUS evidence hard-codes:

- `authority=research_only`
- `production_authorized=false`
- `execution_allowed=false`

## Current infrastructure caveat

As of 2026-10-05, GitHub accepted and scheduled this private-repository workflow
but GitHub-hosted jobs failed before usable step logs were produced. A temporary
bare runner probe failed the same way, while the public AION workflow executed
normally. The workflow itself remains installed; private-repository runner
eligibility/quota/settings must permit a hosted runner before these gates can
execute.

## Dependency maintenance automation

Dependabot checks GitHub Actions and Python packaging metadata every Monday in
`America/Chicago`. Minor and patch updates are grouped to reduce pull-request
noise; major updates remain isolated for explicit review. Dependency changes that
touch `pyproject.toml` or workflow files are still subject to the repository's
normal assurance gates before merge.

