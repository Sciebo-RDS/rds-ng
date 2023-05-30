#!/usr/bin/env python3
# This script performs static type checks on all components.
# If a check fails, the process will exit with a non-zero return code.
#
# Note that Python 3 and the 'pytype' library (simply run `pip install pytype`) are required to run this script.

import subprocess
import sys
import json


def get_components():
    with open("./config/meta-information.json") as f:
        data = json.load(f)
        return data["components"]
    return {}


if __name__ == "__main__":
    for appid, info in get_components().items():
        comp_dir = f"./src/{info['directory']}"
        print(f"Type-checking component '{info['name']} ({appid})' in {comp_dir}...", flush=True)

        retcode = subprocess.call(["python3", "-m", "pytype", "-n", comp_dir])
        if retcode != 0:
            sys.exit(retcode)

        print("---", flush=True)
