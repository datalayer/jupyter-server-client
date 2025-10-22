# Jupyter Server Client - Test Commands
#
# Usage:
#   make test          # Run all tests
#   make test-verbose  # Run tests with verbose output
#   make test-coverage # Run tests with coverage report
#   make test-specific TEST=test_kernels  # Run specific test module

# Default Python executable
PYTHON := python3

# Test directory
TEST_DIR := tests

.PHONY: test test-verbose test-coverage test-specific help clean

# Default target
help:
	@echo "Available targets:"
	@echo "  test          - Run all tests"
	@echo "  test-verbose  - Run tests with verbose output"
	@echo "  test-coverage - Run tests with coverage report"
	@echo "  test-specific - Run specific test (use TEST=test_name)"
	@echo "  clean         - Clean up test artifacts"
	@echo ""
	@echo "Examples:"
	@echo "  make test"
	@echo "  make test-specific TEST=test_kernels"
	@echo "  make test-coverage"

# Run all tests
test:
	@echo "🧪 Running jupyter-server-client tests..."
	cd $(TEST_DIR) && $(PYTHON) run_tests.py

# Run tests with verbose output
test-verbose:
	@echo "🧪 Running jupyter-server-client tests (verbose)..."
	cd $(TEST_DIR) && $(PYTHON) -m unittest discover -v

# Run tests with coverage (requires coverage package)
test-coverage:
	@echo "🧪 Running tests with coverage..."
	coverage run --source=../jupyter_server_client -m unittest discover $(TEST_DIR)
	coverage report -m
	coverage html

# Run specific test
test-specific:
ifndef TEST
	@echo "❌ Please specify TEST variable. Example: make test-specific TEST=test_kernels"
	@exit 1
endif
	@echo "🧪 Running specific test: $(TEST)"
	cd $(TEST_DIR) && $(PYTHON) -m unittest $(TEST) -v

# Clean up test artifacts
clean:
	@echo "🧹 Cleaning up test artifacts..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf htmlcov/
	rm -f .coverage

# Install test dependencies (optional)
install-test-deps:
	@echo "📦 Installing test dependencies..."
	pip install -r $(TEST_DIR)/requirements.txt

publish-pypi: # publish the pypi package
	git clean -fdx && \
		python -m build
	@exec echo
	@exec echo twine upload ./dist/*-py3-none-any.whl
	@exec echo
	@exec echo https://pypi.org/project/jupyter-server-client/#history

