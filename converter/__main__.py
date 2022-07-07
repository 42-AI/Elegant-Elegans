from converter.checker import path_checker, path_inside_checker
from converter.convert import tiff_images_to_video
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

    # # Convert tiff images to video
    # video_name = '' # Example : "vid1"
    # format = '' # Value expected : "mp4", "avi"
    # tiff_images_to_video((dir_path, video_name, format, metadata)


# ########################################################################## #
#                                   MAIN                                     #
# ########################################################################## #

if __name__ == "__main__":
    main()
