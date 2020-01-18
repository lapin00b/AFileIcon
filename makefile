all:
  python build -i -p

icons:
  python build -i

preferences:
  python build -p

check:
  black --check --exclude "/(\.git.*|\.mypy_cache|\.nox|\.tox|\.venv|vendor)/" .
