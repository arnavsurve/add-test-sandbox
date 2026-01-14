#!/bin/bash

# Test script for FastAPI Photo Blog
# This script sets up the environment and runs all tests

set -e

echo "=================================="
echo "FastAPI Photo Blog - Test Runner"
echo "=================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Run pytest tests
echo "Running pytest tests..."
pytest test_main.py -v --tb=short
PYTEST_EXIT=$?
echo ""

if [ $PYTEST_EXIT -eq 0 ]; then
    echo "✓ All pytest tests passed!"
else
    echo "✗ Some pytest tests failed"
    exit 1
fi

# Start server in background for integration tests
echo ""
echo "Starting FastAPI server for integration tests..."
python3 main.py &
SERVER_PID=$!

# Give server time to start
sleep 3

# Run integration tests
echo "Running integration tests..."
python3 test_api.py
INTEGRATION_EXIT=$?

# Stop the server
kill $SERVER_PID 2>/dev/null || true

echo ""
if [ $INTEGRATION_EXIT -eq 0 ]; then
    echo "✓ All integration tests passed!"
else
    echo "✗ Some integration tests failed"
    exit 1
fi

echo ""
echo "=================================="
echo "✓ ALL TESTS PASSED SUCCESSFULLY!"
echo "=================================="
