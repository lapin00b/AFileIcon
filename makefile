all:
  python -u build -i -p

icons:
  python -u build -i

preferences:
  python -u build -p

check:
  black --check --exclude "/(\.git.*|\.mypy_cache|\.nox|\.tox|\.venv|vendor)/" .
