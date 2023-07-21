#!/usr/bin/env python3
# This script performs static type checks on all components.
# If a check fails, the process will exit with a non-zero return code.
#
# Note that Python 3 and the 'pytype' library (simply run `pip install pytype`) are required to run this script.

import subprocess
import sys
import json


def get_components():
    """
    Gets a list of all components present (as listed in *meta-information.json*).
    """
    with open("./config/meta-information.json", encoding="utf-8") as file:
        data = json.load(file)
        return data["components"]


if __name__ == "__main__":
    for appid, info in get_components().items():
        comp_dir = f"./src/{info['directory']}"
        print(f"Type-checking component '{info['name']} ({appid})' in {comp_dir}...", flush=True)

        ret_code = subprocess.call(["python3", "-m", "pytype", "-n", comp_dir])
        if ret_code != 0:
            sys.exit(ret_code)

        print("---", flush=True)
