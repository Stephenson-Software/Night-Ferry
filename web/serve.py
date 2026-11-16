#!/usr/bin/env python3
# @author Daniel McCoy Stephenson
"""Serve the browser build: python3 web/serve.py, then open the URL printed.

Hands out web/index.html, web/game.zip and the tak assets at /tak/, with the
COOP/COEP headers the Pyodide front-end needs. It never runs the game; the
player's browser does. NIGHTFERRY_WEB_HOST / NIGHTFERRY_WEB_PORT move it.

It takes no arguments: -h/--help prints the usage and exits, and anything
else is refused, so a mistyped flag never leaves a server holding the port."""
import os
import sys

from tak.web.serve import main

REPOSITORY_ROOT = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)

USAGE = """Usage: python3 web/serve.py

Serves the browser build of Night Ferry (build it first with
python3 web/build_zip.py) at http://127.0.0.1:8080/ until Ctrl+C.
NIGHTFERRY_WEB_HOST / NIGHTFERRY_WEB_PORT change the address."""

if __name__ == "__main__":
    if sys.argv[1:] in (["-h"], ["--help"]):
        print(USAGE)
        sys.exit(0)
    if sys.argv[1:]:
        print(USAGE, file=sys.stderr)
        sys.exit(2)
    main(REPOSITORY_ROOT, title="Night Ferry", envPrefix="NIGHTFERRY")
