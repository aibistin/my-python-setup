# src/my_python_setup/wikipedia.py
"""Client for the Wikipedia REST API, Version 1."""

from dataclasses import dataclass


import click
import desert
import marshmallow
import requests

# from typing import Any

API_URL: str = "https://{language}.wikipedia.org/api/rest_v1/page/random/summary"


@dataclass
class Page:
    """Page Resource.

    Attributes:
    title: The title of the wikipedia page
    extract: A plain text summary.
    """

    title: str
    extract: str


schema = desert.schema(Page, meta={"unknown": marshmallow.EXCLUDE})


def get_random_page(language: str = "en") -> Page:
    """Return a random page.

    Perform a GET request to the page random summary endpoint.

    Args:
        language: The Wikipedia language edition. The default
            language is "en" for English.

    Returns:
        A Page resource.

    Raises:
        ClickException: The HTTP reauest failed or the response contained
            no or an invalid value in the body.

    Example:
        >>> from my_python_setup import wikipedia
        >>> page = wikipedia.random_page(language="en")
        >>> bool(page.title)
        True
    """
    url = API_URL.format(language=language)

    try:
        with requests.get(url) as response:
            response.raise_for_status()
            data = response.json()
            return schema.load(data)
    except (requests.RequestException, marshmallow.ValidationError) as error:
        message = str(error)
        raise click.ClickException(message)
