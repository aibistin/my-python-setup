# tests/conftest.py
# Note: This 'conftest.py' config module is autodiscoverable by Python
"""Package-wide text fixtures."""
from unittest.mock import Mock


from _pytest.config import Config
import pytest
from pytest_mock import MockFixture


def pytest_configure(config: Config) -> None:
    """Pytest configuration hook."""
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")


@pytest.fixture
def mock_requests_get(mocker: MockFixture) -> Mock:
    """Fixture for mocking requests get."""
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Wicked Wicki",
        "extract": "The Wicked Wicki whacked the whacky tricky API",
    }
    return mock
