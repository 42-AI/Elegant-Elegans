import argparse

# ########################################################################## #
#                                CONSTANTS                                   #
# ########################################################################## #


# ########################################################################## #
#                                FUNCTIONS                                   #
# ########################################################################## #

def parser() -> dict:
    """ [Description]
    Return:
    -------
    """
    # use argparse.ArgumentParser()
    # then add_argument method
    # see https://docs.python.org/3/library/argparse.html
    return parser.parse_args()


def path_checker(path: str):
    """ [Description]

    Arguments:
    ----------
        path (str): path to the directory
    Raise:
    ------
        Depends on the kind of issue encountered:
        * NotADirectoryError if ...
        * PermissionError if ...
    """
    pass


def path_inside_checker(dir_path):
    """ [Description]
    
    Arguments:
    ----------
        ...
    Raises:
        ...
    """
    pass


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


import argparse

# ########################################################################## #
#                                   MAIN                                     #
# ########################################################################## #

if __name__=="__main__":
    args = parser()

    # print(args)
    dir_path = args.path
    metadata = loadMetadata(dir_path)
    checkImages(metadata, dir_path)
