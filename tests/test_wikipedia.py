# tests/test_wikipedia.py

from my_python_setup import wikipedia


def test_random_pages_uses_given_language(mock_requests_get):
    wikipedia.get_random_page(language="ga")
    args, _ = mock_requests_get.call_args
    assert "ga.wikipedia.org" in args[0]
