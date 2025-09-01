# pbiviz_cli.py
# Helpers para invocar pbiviz CLI
import subprocess

def run_pbiviz(args):
    cmd = ["pbiviz"] + args
    return subprocess.run(cmd, capture_output=True)
