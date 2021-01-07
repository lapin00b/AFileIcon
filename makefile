all:
	python build -i -p

icons:
	python build -i

preferences:
	python build -p

check:
	black --check .
