#!/usr/bin/env python3
# This script performs static type checks on all components.
# If a check fails, the process will exit with a non-zero return code.
#
# Note that Python 3 and the 'pytype' library (simply run `pip install pytype`) are required to run this script.

import subprocess
import sys

# All Python components to be checked need to be listed in this array
components = ["gate"]

for component in components:
    print(f"Type-checking component '{component}'...", flush=True)

    retcode = subprocess.call(["python3", "-m", "pytype", "-n", f"./src/{component}"])
    if retcode != 0:
        sys.exit(retcode)

    print("---", flush=True)
