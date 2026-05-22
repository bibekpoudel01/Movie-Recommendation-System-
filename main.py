import os
import runpy
import sys

BASE_DIR = os.path.dirname(__file__)
UI_DIR = os.path.join(BASE_DIR, "ui")
UI_APP_PATH = os.path.join(UI_DIR, "ui_app.py")
if UI_DIR not in sys.path:
    sys.path.insert(0, UI_DIR)
runpy.run_path(UI_APP_PATH, run_name="__main__")


