import os
import subprocess
import sys
import zipfile

from conftest import REPOSITORY_ROOT


def test_the_page_uses_the_kits_assets_and_names_the_game():
    with open(os.path.join(REPOSITORY_ROOT, "web", "index.html")) as f:
        page = f.read()
    assert "<title>Night Ferry</title>" in page
    for asset in ("/tak/client.css", "/tak/client.js", "/tak/boot.js"):
        assert asset in page, asset
    assert 'idbName: "night-ferry-saves"' in page
    assert 'saveDirEnv: "NIGHTFERRY_SAVE_DIR"' in page
    assert 'entry: "web/pyodide_main.py"' in page


def test_the_bundle_carries_the_game_and_the_kit(tmp_path):
    from tak.web.bundle import build

    output = build(
        REPOSITORY_ROOT,
        outputPath=str(tmp_path / "game.zip"),
        extraFiles=("version.txt", "web/pyodide_main.py"),
    )
    with zipfile.ZipFile(output) as bundle:
        names = set(bundle.namelist())
    for required in (
        "src/nightferry/game.py",
        "src/nightferry/scenes/saloon.py",
        "src/tak/ui/pyodide.py",
        "src/tak/web/assets/client.js",
        "schemas/save.json",
        "web/pyodide_main.py",
        "version.txt",
    ):
        assert required in names, required


def test_build_zip_script_runs():
    result = subprocess.run(
        [sys.executable, os.path.join("web", "build_zip.py")],
        cwd=REPOSITORY_ROOT,
        env=dict(os.environ),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    assert result.returncode == 0, result.stderr
    assert os.path.exists(os.path.join(REPOSITORY_ROOT, "web", "game.zip"))


def test_pyodide_entry_point_builds_the_pyodide_front_end():
    with open(os.path.join(REPOSITORY_ROOT, "web", "pyodide_main.py")) as f:
        source = f.read()
    assert "UIType.PYODIDE" in source and "NightFerry(" in source


def test_the_page_credits_the_author_outside_the_game_area():
    with open(os.path.join(REPOSITORY_ROOT, "web", "index.html")) as f:
        page = f.read()
    credit = '<a href="https://danielstephenson.dev">danielstephenson.dev</a>'
    assert "More by Daniel Stephenson &rarr; " + credit in page
    assert page.index(credit) > page.index('<div id="app"></div>')
