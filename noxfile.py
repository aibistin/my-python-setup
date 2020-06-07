# noxfile.py
import tempfile

import nox

# For end to end testing
# nox -rs tests-3.8 -- -m e2e
# For running a specific test module
# nox -- tests/test_console.py
# For re-using the test environment
# nox -r
# To run a lint check
# nox -rs lint


locations = "src", "tests", "noxfile.py"
nox.options.sessions = "lint", "safety", "tests"


def install_with_constraints(session, *args, **kwargs):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


# @nox.session(python=["3.8", "3.7"])
@nox.session(python=["3.8"])
def tests(session):
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session, "coverage[toml]", "pytest", "pytest-cov", "pytest-mock"
    )
    session.run("pytest", *args)


@nox.session(python=["3.8"])
def lint(session):
    args = session.posargs or locations
    install_with_constraints(
        session, "flake8", "flake8-black", "flake8-bugbear", "flake8-import-order"
    )
    session.run("flake8", *args)


@nox.session(python=["3.8"])
def black(session):
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


# Create a temporary constraints file
@nox.session(python="3.8")
def safety(session):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")
