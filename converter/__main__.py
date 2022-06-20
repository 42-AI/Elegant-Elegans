from converter.checker import path_checker, path_inside_checker
from converter.parser import parser


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

    # checker of the inside of the path
    path_inside_checker(dir_path)

    # # Parsing the json metadata file
    # metadata = json_parser(dir_path)

    # # checker of the tiff images based on metadata
    # tiff_files_checker(metadata)


# ########################################################################## #
#                                   MAIN                                     #
# ########################################################################## #

if __name__ == "__main__":
    main()
