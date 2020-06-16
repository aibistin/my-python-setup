# tests/test_console.py
"""Test cases for the console module."""
from unittest.mock import Mock


import click
import click.testing
from click.testing import CliRunner
import pytest
from pytest_mock import MockFixture
import requests


from my_python_setup import console


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner: CliRunner) -> None:
    """It exits with a status code of 0."""
    result = runner.invoke(console.main)
    assert result.exit_code == 0


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking the CLI."""
    return click.testing.CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker: MockFixture) -> Mock:
    """It returns a random page."""
    return mocker.patch("my_python_setup.wikipedia.get_random_page")


def test_main_succeeds(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It returns a rc of 0."""
    runner = click.testing.CliRunner()
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It returns the correct result optput."""
    result = runner.invoke(console.main)
    assert "Wicked" in result.output
    assert "whacky" in result.output


def test_main_invokes_request_get(runner: CliRunner, mock_requests_get: Mock) -> None:
    """Mock requests get called."""
    runner.invoke(console.main)
    assert mock_requests_get.called


def test_main_calls_en_wikipedia_org(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    """en.wikipedia.org gets called."""
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_main_fails_on_request_error(
    runner: CliRunner, mock_requests_get: None
) -> None:
    """Result has an exit_code of 1."""
    mock_requests_get.side_effect = Exception("Trumpanzee!!!")
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(
    runner: CliRunner, mock_requests_get
) -> None:
    """There is an Error in the result output."""
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output


def main_gets_specified_language(
    runner: CliRunner, mock_wikipedia_random_page: Mock
) -> None:
    """Main gets the specified language."""
    runner.invoke(console.main, ["--language=cr"])
    mock_wikipedia_random_page.assert_called_with(language="cr")
