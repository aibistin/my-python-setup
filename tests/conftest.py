# tests/conftest.py
# Note: This 'conftest.py' config module is autodiscoverable by Python
import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")


@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Wicked Wicki",
        "extract": "The Wicked Wicki whacked the whacky tricky API",
    }
    return mock
