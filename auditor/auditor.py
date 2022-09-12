import os

NB_LIMIT = 10

# Checker related to the argument parsed.
def path_checker(path: str):
    """Check the existence and access of a directory.

    Arguments:
        path (str): path to the input directory (containing the images).

    Raises:
        NotADirectoryError: directory doesn't exist or is not a directory.
        PermissionError: user doesn't have access to the directory.
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
        FileNotFoundError: there is no .json file
        Exception: there are fewer than 100 .tif files
        Exception a file other than .tif or .json
    """
    number_tif_files = 0
    metadata_file = False
    for file in os.listdir(dir_path):
        if file[-4:] == ".tif":
            number_tif_files += 1
        elif file == "metadata.txt":
            metadata_file = True
        elif file[-5:] == ".json":
            continue
        else:
            raise Exception("File other than .tif or .json or metadata.txt found")
    if metadata_file is False:
        raise FileNotFoundError("No metadata file found")
