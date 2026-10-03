import os


# @author Daniel McCoy Stephenson
class Config:
    def __init__(self):
        # NIGHTFERRY_SAVE_DIR relocates the whole save directory - a mounted
        # volume for a server install, or the Worker-side directory that the
        # Pyodide front-end mirrors to the browser's IndexedDB.
        self.dataDirectory = os.environ.get("NIGHTFERRY_SAVE_DIR") or "data"
