"""Pytest configuration for async tests."""
import pytest

# Configure pytest-asyncio to use auto mode instead of strict
pytest_plugins = ('pytest_asyncio',)

def pytest_configure(config):
    """Configure pytest."""
    config.option.asyncio_mode = "auto"
