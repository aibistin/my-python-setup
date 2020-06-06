# tests/test_console.py
import click.testing
import pytest
import requests

from my_python_setup import console

@pytest.fixture
def runner():
    return click.testing.CliRunner()

@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title" : "Wicked Wicki", 
        "extract": "The Wicked Wicki whacked the whacky tricky API", 
    }
    return mock

@pytest.fixture
def mock_wikipedia_random_page(mocker):
    return mocker.patch("my_python_setup.wikipedia.random_page")


def test_main_succeeds(runner, mock_requests_get):
    runner = click.testing.CliRunner()
    result = runner.invoke(console.main)
    assert "Wicked" in result.output
    assert "whacky" in result.output
    assert result.exit_code == 0

def test_main_prints_title(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert "Wicked" in result.output
    assert "whacky" in result.output

def test_main_invokes_request_get(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert mock_requests_get.called

def test_main_calls_en_wikipedia_org(runner, mock_requests_get):
    result = runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert 'en.wikipedia.org' in args[0]

def test_main_fails_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = Exception("Trumpanzee!!!")
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_fails_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = Exception("Trumpanzee!!!")
    result = runner.invoke(console.main)
    assert result.exit_code == 1

def test_main_prints_message_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output

def main_gets_specified_language(runner, mock_wikipedia_random_page):
    runner.invoke(console.main, ["--language=cr"])
    mock_wikipedia_random_page.assert_called_with(language="cr")



