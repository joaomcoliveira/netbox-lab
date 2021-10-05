# Makefile to run below targets

# Default goal runs the "test" target
.DEFAULT_GOAL := test

.PHONY: test
test: clean lint unit

.PHONY: lint
lint:
	@echo "Starting lint"
	-find . -name "*.py" | xargs pylint
	find . -name "*.py" | xargs black
	@echo "Completed lint"

.PHONY: unit
unit:
	@echo "Starting unit tests"
	python3 -m pytest tests/ --verbose
	@echo "Completed unit tests"

.PHONY: clean
clean:
	@echo "Starting clean"
	find . -name "*.pyc" | xargs -r rm
	rm -f nornir.log
	@echo "Completed clean"
