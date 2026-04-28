# upd-pre-commit

A [pre-commit](https://pre-commit.com/) hook for [upd](https://github.com/rvben/upd), a fast multi-ecosystem dependency updater written in Rust.

## Usage

To use upd with pre-commit, add the following to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/rvben/upd-pre-commit
    rev: v0.1.5
    hooks:
      - id: upd-check        # Fail if any dependencies are outdated
      - id: upd-check-major  # Fail only on major (breaking) updates
```

Two hooks are available:
- **`upd-check`** — Fails if any dependencies are outdated (runs on pre-push)
- **`upd-check-major`** — Fails only on major (breaking) updates (runs on pre-push)

You can customize which ecosystems to check:

```yaml
repos:
  - repo: https://github.com/rvben/upd-pre-commit
    rev: v0.1.5
    hooks:
      - id: upd-check
        args: ['--lang', 'python', '--lang', 'rust']
```

## Supported Ecosystems

upd supports 10 ecosystems: Python, Node.js, Rust, Go, Ruby, .NET, Terraform, GitHub Actions, pre-commit, and Mise/asdf.

## Installation

When you run `pre-commit install` or `pre-commit run`, pre-commit will automatically install `upd` in an isolated Python environment using pip. You do **not** need to install upd manually.

## License

MIT (see [LICENSE](LICENSE))
