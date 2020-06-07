# noxfile.py
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


# @nox.session(python=["3.8", "3.7"])
@nox.session(python=["3.8"])
def tests(session):
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session(python=["3.8"])
def lint(session):
    args = session.posargs or locations
    session.install("flake8")
    session.run("flake8", *args)
