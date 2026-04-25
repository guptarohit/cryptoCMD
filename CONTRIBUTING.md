# Contributing

Thanks for contributing to `cryptoCMD`.

## Setting up locally

```bash
git clone https://github.com/guptarohit/cryptoCMD.git
cd cryptoCMD
uv sync
```

## Before opening a PR

- Run the linter: `uv run ruff check .`
- Run the formatter: `uv run ruff format .`
- Run the example scripts to verify data fetching works:
  ```bash
  uv run python examples/get_csv.py
  uv run python examples/get_by_coin_name.py
  uv run python examples/get_by_id_number.py
  ```
- Keep changes focused and backward compatible where possible.

## Pull request titles

This repository uses Conventional Commit style PR titles because release automation relies on them.

Examples:

- `feat: add support for OHLCV export format`
- `fix: handle missing quote data gracefully`
- `docs: update README with new fiat examples`
- `refactor: simplify pagination logic`
- `test: add coverage for invalid fiat code`

Recommended types:

- `feat`
- `fix`
- `docs`
- `test`
- `refactor`
- `perf`
- `build`
- `ci`
- `chore`
- `deps`
- `revert`

If a PR title is not in the expected format, maintainers may edit it before merge.

## Commit messages

Conventional Commit style commit messages are welcome, but not required.

Release automation relies on the **pull request title**, so contributors do not need to rewrite individual commits to match the release format.

Versioning notes:

- `feat` → minor release
- `fix` → patch release
- `feat!` or `BREAKING CHANGE` → major release

## Merge guidance for maintainers

If merge commits are used, keep the final merge commit title aligned with the PR title so release automation can infer the release correctly from git history.

## Release process

Releases are fully automated:

- `release-please` watches commits on `master` and opens a release PR updating `CHANGELOG.md` and the version in `pyproject.toml` and `cryptocmd/__version__.py`
- Merging the release PR creates the git tag and GitHub Release
- The tag triggers the release workflow which builds the package and publishes it to PyPI via Trusted Publishers

Please do not manually edit `CHANGELOG.md` for normal releases unless intentionally correcting release notes.
