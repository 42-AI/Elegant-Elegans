from converter.checker import path_checker, path_inside_checker
from converter.convert import tiff_images_to_video
from converter.json_parser import load_metadata, check_images
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

    # load the json metadata file
    metadata = load_metadata(dir_path)

    # # checker of the tiff images based on metadata. Retrieving some info about frames
    stat_frames = check_images(metadata)

    # Convert tiff images to video
    video_name = args.output # Example : "vid1"
    format = args.format # Value expected : "mp4", "avi"
    tiff_images_to_video(dir_path, video_name, format, stat_frames)


# ########################################################################## #
#                                   MAIN                                     #
# ########################################################################## #

if __name__ == "__main__":
    main()
