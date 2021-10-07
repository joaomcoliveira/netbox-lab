# Makefile to run below targets

# Default goal runs the "all" target
.DEFAULT_GOAL := all

.PHONY: all
all: clean lint test

.PHONY: lint
lint:
	@echo "Starting lint"
	-find . -name "*.py" | xargs pylint
	-find . -name "*.py" | xargs black --check
	@echo "Completed lint"

.PHONY: test
test:
	@echo "Starting unit tests"
	python3 -m pytest tests/ --verbose
	@echo "Completed unit tests"

.PHONY: clean
clean:
	@echo "Starting clean"
	find . -name "*.pyc" | xargs -r rm
	rm -f nornir.log
	@echo "Completed clean"
