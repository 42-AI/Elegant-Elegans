import argparse
from converter.convert import tiff_images_to_video

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


# ########################################################################## #
#                                   MAIN                                     #
# ########################################################################## #

if __name__ == '__main__':
    # parsing the argument(s)
    args = parser()
    dir_path = args['path']

    # checker of the path
    path_checker(dir_path)

    # checker of the inside of the path
    path_inside_checker(dir_path)

    # Parsing the json metadata file
    metadata = json_parser(dir_path)

    # checker of the tiff images based on metadata
    tiff_files_checker(metadata)
    

    video_name = ''
    format = ''
    # convert tiff images to video
    tiff_images_to_video(dir_path, video_name, format, metadata)