"""Copy example.py to a temporary directory."""

import os
import shutil

PROJECT_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
EXAMPLE_PATH = os.path.join(PROJECT_PATH, "example.py")
TEMP_DIR = os.getenv("RUNNER_TEMP")
EXAMPLE_DEST = os.path.join(TEMP_DIR, "test_example")

os.mkdir(EXAMPLE_DEST)
shutil.copy(EXAMPLE_PATH, EXAMPLE_DEST)
