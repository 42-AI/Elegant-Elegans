import argparse
import sys
import os

# ########################################################################## #
#                                CONSTANTS                                   #
# ########################################################################## #

NB_LIMIT = 100

# ########################################################################## #
#                                FUNCTIONS                                   #
# ########################################################################## #

def parser() -> dict:
    """ [Description]
        Parse arguments to get name directory as input and the video file's
        name as output
    Return:
    -------
        A dictionary containing the name of the path to input directory
        and the defined name of the video file as output
        Namespace(output='', path='')
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--path")
    parser.add_argument("-o", "--output")
    return (parser.parse_args())


def path_checker(path: str):
    """ [Description]
        Check the existence and access of a directory
    Arguments:
    ----------
        path (str): path to the directory
    Raise:
    ------
        Depends on the kind of issue encountered:
        * NotADirectoryError if the directory doesn't exist or is not a directory
        * PermissionError if the user doesn't have access to the directory
    """
    if not os.path.isdir(path):
        raise NotADirectoryError(path + " is not a directory.")
    if not os.access(path, os.R_OK | os.W_OK):
        raise PermissionError("Permission denied to " + path)


def path_inside_checker(dir_path):
    """ [Description]
        Check that the files inside the directory are .tiff or .json,
        that a .json file exists and that there are at least 100 .tiff files
    Arguments:
    ----------
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


def json_parser(dir_path):
    """ [Description]
    
    Arguments:
    ----------
        ...
    Raises:
        ...
    """
    pass


def tiff_files_checker(metadata):
    """ [Description]
    
    Arguments:
    ----------
        ...
    Raises:
        ...
    """
    pass


# ########################################################################## #
#                                   MAIN                                     #
# ########################################################################## #

if __name__ == '__main__':
    # parsing the argument(s)
    args = parser()

    # print(args)
    dir_path = args.path

    # checker of the path
    path_checker(dir_path)

    # checker of the inside of the path
    path_inside_checker(dir_path)

    # # Parsing the json metadata file
    # metadata = json_parser(dir_path)

    # # checker of the tiff images based on metadata
    # tiff_files_checker(metadata)
    
