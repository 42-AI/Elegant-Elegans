import argparse
import json
from datetime import datetime

import cv2 as cv


# ########################################################################### #
#                          Parsing of the inputs of converter                 #
# ########################################################################### #
#           Parser related to the arguments of converter program
def parser() -> dict:
    """Parse arguments to get name directory as input and the video file's name as output.

    Return:
        A dictionary containing the name of the path to input directory
        and the defined name of the video file as output
        Namespace(output='', path='')
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path", type=str, required=True, help="path where source will be look in."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Name of the converted video (without the video format).",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        required=False,
        default="mp4",
        choices=["mp4", "avi"],
        help="format of the generated video.",
    )
    return parser.parse_args()


# ########################################################################### #
#                          Parsing of the inputs of converter                 #
# ########################################################################### #


def load_metadata(directoryPath: str) -> dict:
    """Loads the metadata file in a python dictionary.

    Args:
        directoryPath (str): directory path to json file to load.

    Raises:
        Exception: raise an error if an unknown format is passed.

    Returns:
        dict: the loaded metadata.
    """
    try:
        file_path = directoryPath + "/metadata.txt"
        metadata = json.load(open(file_path))
    except:
        raise Exception("Error trying to load metadata.txt")
    return metadata


def check_images(metadata: dict, directoryPath: str) -> dict:
    """Checks if the images respect the information in the metadata.

    Args:
        metadata: the metadata resulting from loadMetadata
        directoryPath: the directory where the images are located

    Returns:
        dict: a dictionary with the validated metadata
    """
    total_time_ms = 0
    expect_frame_no = 0
    expected_frames = metadata["Summary"]["Frames"]
    filenames_list = []

    for obj in metadata:
        if obj.startswith("Metadata-Default"):
            filename = obj.rsplit("/", 1)[-1]
            if filename != "Summary":
                cv_img = cv.imread(directoryPath + "/" + filename)
                if cv_img is None:
                    raise FileNotFoundError(f"Could not load file: {directoryPath}/{filename}")
                filenames_list.append(filename)

                # Checking the shape of the image and the expected shape
                actual_height, actual_width = cv_img.shape[0], cv_img.shape[1]
                expected_width = metadata[obj]["Width"]
                expected_height = metadata[obj]["Height"]
                if (actual_height != expected_height) or (actual_width != expected_width):
                    raise Exception(f"Mismatched image size: frame: {directoryPath}/{filename}")

                currentFrame = metadata[obj]["Frame"]
                if currentFrame == 0:
                    time_to_first_image = metadata[obj]["ElapsedTime-ms"]

                # checks for missing frames
                if currentFrame != expect_frame_no:
                    raise Exception(
                        f"Mismatched frame number: expected frame no: {expect_frame_no} but got frame no: {currentFrame}"
                    )
                total_time_ms = metadata[obj]["ElapsedTime-ms"] - time_to_first_image
                expect_frame_no = expect_frame_no + 1

    if expect_frame_no != expected_frames:
        raise Exception(
            f"Mismatched between the number of expected frames ({expected_frames}) and the actual number ({frames})"
        )
    print("all expected frames were found")
    print("total capture time: ", total_time_ms)
    return {
        "avg_fps": expect_frame_no / (total_time_ms / 1000),
        "frame_width": expected_width,
        "frame_height": expected_height,
        "frame_names": filenames_list,
    }
