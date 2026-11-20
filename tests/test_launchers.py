"""The launchers - web/serve.py, web/build_zip.py and run.sh - answer
-h/--help with a usage string and refuse arguments they do not take, instead
of starting a server, a game or a build nobody asked for.

Every run has a timeout: a launcher that ignored its arguments would start
serving or playing, and the test fails on the timeout rather than hanging.
A build that ignored them would overwrite web/game.zip, so those tests check
the bundle is left exactly as it was."""

import os
import subprocess
import sys

import pytest

from conftest import REPOSITORY_ROOT

SERVE = [sys.executable, os.path.join("web", "serve.py")]
BUILD = [sys.executable, os.path.join("web", "build_zip.py")]
BUNDLE = os.path.join(REPOSITORY_ROOT, "web", "game.zip")
RUN = ["bash", "run.sh"]


def _run(command):
    return subprocess.run(
        command,
        cwd=REPOSITORY_ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        timeout=20,
    )


@pytest.mark.parametrize("flag", ["-h", "--help"])
def test_serve_prints_its_usage_for_help_and_serves_nothing(flag):
    result = _run(SERVE + [flag])
    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith("Usage: python3 web/serve.py")
    assert "NIGHTFERRY_WEB_PORT" in result.stdout
    assert "is being served" not in result.stdout


@pytest.mark.parametrize("arguments", [["--port", "9000"], ["web"]])
def test_serve_refuses_arguments_it_does_not_take(arguments):
    result = _run(SERVE + arguments)
    assert result.returncode == 2
    assert result.stderr.startswith("Usage: python3 web/serve.py")
    assert "is being served" not in result.stdout


def _bundleStamp():
    """The bundle's modification time, or None while there is no bundle."""
    try:
        return os.stat(BUNDLE).st_mtime_ns
    except FileNotFoundError:
        return None


@pytest.mark.parametrize("flag", ["-h", "--help"])
def test_build_zip_prints_its_usage_for_help_and_builds_nothing(flag):
    before = _bundleStamp()
    result = _run(BUILD + [flag])
    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith("Usage: python3 web/build_zip.py")
    assert "python3 web/serve.py" in result.stdout
    assert _bundleStamp() == before


@pytest.mark.parametrize("arguments", [["--out", "other.zip"], ["web"]])
def test_build_zip_refuses_arguments_it_does_not_take(arguments):
    before = _bundleStamp()
    result = _run(BUILD + arguments)
    assert result.returncode == 2
    assert result.stderr.startswith("Usage: python3 web/build_zip.py")
    assert result.stdout == ""
    assert _bundleStamp() == before


@pytest.mark.parametrize("flag", ["-h", "--help"])
def test_run_prints_its_usage_for_help_and_plays_nothing(flag):
    result = _run(RUN + [flag])
    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith("Usage: ./run.sh")
    assert "./run.sh web" in result.stdout


@pytest.mark.parametrize("arguments", [["wbe"], ["web", "extra"]])
def test_run_refuses_arguments_it_does_not_take(arguments):
    result = _run(RUN + arguments)
    assert result.returncode == 2
    assert result.stderr.startswith("Usage: ./run.sh")
    assert result.stdout == ""
