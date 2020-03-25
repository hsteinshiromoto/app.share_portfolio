# ---
# Import
# ---

# Infrastructure Modules
import pathlib
from pathlib import Path
import os
import glob
import re
import yaml

# ---
# Global Definitions
# ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# ---
# Functions and classes
# ---
def get_file(path: pathlib.PosixPath, pattern: str=None, extension: str=None,
             latest: bool=True):
    """
    Find (latest) files with a pattern

    :param path:
    :param pattern:
    :param extension:
    :param latest:
    :return: str or list
    """

    if not extension:
        extension = ""

    list_file_names = glob.glob(f"{path}/*{extension}")

    if not list_file_names:
        return None

    elif pattern:
        list_pattern = [file_name for file_name in
                        list_file_names if re.search(pattern, file_name)]

        list_file_names = list_pattern

        if not list_file_names:
            list_file_names = None

    if latest == True:
        output = os.path.basename(max(list_file_names,
                                      key=os.path.getctime))

    else:
        output = [os.path.basename(item) for item in list_file_names]

    print("Found file(s) {}.".format(output))

    return output


def get_config(path: pathlib.PosixPath=PROJECT_ROOT / "conf",
               filename: str="config.yaml"):

    with open(str(path / filename)) as config_file:
        config = yaml.safe_load(config_file)

    return config


if __name__ == "__main__":
    conf = get_config()

    print("end")