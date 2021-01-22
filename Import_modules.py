import sys
import subprocess
import pkg_resources

required_modules={
    "yeelight",
    "pyautogui",
    "pillow",
    "pypiwin32",
    "opencv-python"
}

installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required_modules - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing])






