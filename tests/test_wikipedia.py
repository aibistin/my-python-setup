# tests/test_wikipedia.py
"""Test the wikipedia module."""
from unittest.mock import Mock


import click
import pytest


from my_python_setup import wikipedia


def test_random_pages_uses_given_language(mock_requests_get: Mock) -> None:
    """Must return ga.wikipedia.org."""
    wikipedia.get_random_page(language="ga")
    args, _ = mock_requests_get.call_args
    assert "ga.wikipedia.org" in args[0]


def test_random_page_handles_validation_errors(mock_requests_get: Mock) -> None:
    """Validation errors are handled."""
    mock_requests_get.return_value.__enter__.return_value.json.return_value = None
    with pytest.raises(click.ClickException):
        wikipedia.get_random_page()


def test_random_page_returns_page(mock_requests_get: Mock) -> None:
    """Random page returns a Page type."""
    page = wikipedia.get_random_page()
    assert isinstance(page, wikipedia.Page)
