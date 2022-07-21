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
    """Check that the files inside the directory are .tif or .json, that a .json file exists and
    that there are at least 100 .tif files.

    Arguments:
        dir_path : path to directory

    Raises:
        Depends on the kind of issue encountered:
        * If there is no .json file
        * If there are fewer than 100 .tif files
        * If there is a file other than .tif or .json
    """
    num_tif = 0
    metadata = 0
    for file in os.listdir(dir_path):
        if file[-4:] == ".tif":
            num_tif += 1
        elif file == "metadata.txt":
            metadata += 1
        elif file[-5:] == ".json":
            continue
        else:
            raise Exception("File other than .tif or .json or metadata.txt found")
    if metadata == 0:
        raise Exception("No metadata file found")
    if metadata > 1:
        raise Exception("More than one metadata file found")
    if num_tif < NB_LIMIT:
        raise Exception("Number of .tif files insufficient (min required 100)")
