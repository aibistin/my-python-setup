# tests/test_wikipedia.py
import click.testing
import pytest
import requests

from my_python_setup import wikipedia


def test_random_pages_uses_given_language(mock_requests_get):
    wikipekia.random_page(language='ga')
    args, _ = mock_requests_get.call_args
    assert "ga.wikipedia.org" in args[0]

