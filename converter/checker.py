import os

NB_LIMIT = 100

# Checker related to the argument parsed.
def path_checker(path: str):
    """Check the existence and access of a directory.

    Arguments:
        path (str): path to the directory

    Raise:
        Depends on the kind of issue encountered:
        * NotADirectoryError if the directory doesn't exist or is not a directory
        * PermissionError if the user doesn't h—ave access to the directory
    """
    if not os.path.isdir(path):
        raise NotADirectoryError(path + " is not a directory.")
    if not os.access(path, os.R_OK | os.W_OK):
        raise PermissionError("Permission denied to " + path)


def path_inside_checker(dir_path: str):
    """Check that the files inside the directory are .tiff or .json, that a .json file exists and
    that there are at least 100 .tiff files.

    Arguments:
        dir_path : path to directory

    Raises:
        Depends on the kind of issue encountered:
        * If there is no .json file
        * If there are fewer than 100 .tiff files
        * If there is a file other than .tiff or .json
    """
    num_tiff = 0
    num_json = 0
    for file in os.listdir(dir_path):
        if file[-5:] == ".tiff":
            num_tiff += 1
        elif file[-5:] == ".json":
            num_json += 1
        else:
            raise Exception("File other than .tiff or .json found")
    if num_json == 0:
        raise Exception("No .json file found")
    if num_json > 1:
        raise Exception("More than one .json file found")
    if num_tiff < NB_LIMIT:
        raise Exception("Number of .tiff files insufficient (min required 100)")
