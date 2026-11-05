# Contributing to `open-weight-models`

Thank you for helping keep this unofficial enterprise open-weight AI playbook accurate and current!

## What We Welcome

- **Model & License Updates:** New permissive or threshold-gated open-weight model releases, updated MAU/valuation caps, or Tier 4 provenance audits (include a primary link to the official license, model card, or paper).
- **FinOps & Benchmark Corrections:** Updated serverless PayGo vs. self-hosted GPU pricing or benchmark numbers backed by primary public sources.
- **Industry Patterns:** Public engineering blog posts documenting real enterprise production deployments of open-weight models.
- **Series Code Fixes:** Bug fixes, Dockerfile improvements, or clearer setup instructions under `series/`.

For major structural changes or new interactive calculators, please [open an issue](https://github.com/kanchpat/open-weight-models/issues) first so we can align on scope.

## How to Make Changes

> **Important:** `docs/index.html` is generated from `whitepaper/enterprise-playbook.md` and `scripts/build_github_pages.py`. Never hand-edit `docs/index.html` directly, or the next build will overwrite your edits.

1. Fork and clone the repository (requires **Python 3.10+**, standard library only):
   ```bash
   git clone https://github.com/kanchpat/open-weight-models.git
   cd open-weight-models
   ```
2. Edit [`whitepaper/enterprise-playbook.md`](whitepaper/enterprise-playbook.md) (for playbook prose/tables) or [`scripts/build_github_pages.py`](scripts/build_github_pages.py) (for interactive calculators, model cards, or UI layout).
3. Regenerate `docs/index.html` and verify locally:
   ```bash
   python3 scripts/build_github_pages.py
   python3 -m http.server 8000 --directory docs
   ```
4. Open `http://localhost:8000` (`Cmd/Ctrl + Shift + R` to bypass browser cache) and verify:
   - All top navigation anchors and interactive sliders respond cleanly.
   - Primary sources are linked directly in prose/tables.
   - No internal/private URLs or unverified license claims were introduced.
5. Commit both the source change and the regenerated `docs/index.html`, then open a Pull Request against `main`.

## Unofficial Guide Scope & License

This project is an **unofficial community & practitioner guide** (not an officially supported Google product or legal advice). By submitting a pull request, you agree that your contribution is licensed under the [Apache License 2.0](LICENSE).
