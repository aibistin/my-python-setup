# src/my_python_setup/console.py
"""Command Line Interface."""
import textwrap

import click

from . import __version__, wikipedia


@click.command()
@click.option(
    "--language",
    "-l",
    default="en",
    help="Language edition of Wikipedia",
    metavar="LANG",
    show_default=True,
)
@click.version_option(version=__version__)
def main(language: str) -> None:
    """What is this Saucery?"""
    page = wikipedia.get_random_page(language=language)
    # title = data["title"]
    # extract = data["extract"]
    click.secho(page.title, fg="green")
    click.secho(textwrap.fill(page.extract), fg="blue")
