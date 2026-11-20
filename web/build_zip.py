#!/usr/bin/env python3
# @author Daniel McCoy Stephenson
"""Build web/game.zip - the bundle the browser's Pyodide Worker downloads.

    python3 web/build_zip.py

Puts src/, schemas/ and pictures/ in, plus version.txt, art/stills.json and the Worker's entry point,
and the tak package itself (see tak.web.bundle).

It takes no arguments: -h/--help prints the usage and exits, and anything
else is refused, so a mistyped flag never overwrites the bundle."""
import os
import sys

from tak.web.bundle import build

REPOSITORY_ROOT = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)

USAGE = """Usage: python3 web/build_zip.py

Builds web/game.zip, the bundle the browser build of Night Ferry runs
(serve it with python3 web/serve.py). Run it again after any change to
src/, schemas/, pictures/, art/stills.json or version.txt, or a tak upgrade."""

if __name__ == "__main__":
    if sys.argv[1:] in (["-h"], ["--help"]):
        print(USAGE)
        sys.exit(0)
    if sys.argv[1:]:
        print(USAGE, file=sys.stderr)
        sys.exit(2)
    build(
        REPOSITORY_ROOT,
        # pictures/ holds the location stills (RFC 0025); art/stills.json
        # names them and carries their alt text. The scene files they were
        # rendered from stay out of the bundle.
        sourceDirectories=("src", "schemas", "pictures"),
        extraFiles=("version.txt", "web/pyodide_main.py", "art/stills.json"),
    )
