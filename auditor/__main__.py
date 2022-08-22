from os import stat

from auditor.auditor import path_checker
from auditor.parser import audit_images, load_metadata, parser

# ########################################################################## #
#                                FUNCTIONS                                   #
# ########################################################################## #


def main():
    # parsing the argument(s)
    args = parser()

    # print(args)
    dir_path = args.path

    # checker of the path
    path_checker(dir_path)

    # load the json metadata file
    metadata = load_metadata(dir_path)

    # auditor of the tiff images based on metadata.
    # Retrieving some info about frames
    stat_frames = audit_images(metadata, dir_path)


# ########################################################################## #
#                                   MAIN                                     #
# ########################################################################## #

if __name__ == "__main__":
    main()
