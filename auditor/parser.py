import argparse
import json
from cmath import exp
from curses import meta
from json import JSONDecodeError
from os import F_OK, R_OK, access
from os.path import exists as file_exists

import cv2 as cv
import pandas as pd


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
    return parser.parse_args()


# ########################################################################### #
#                          Parsing of the inputs of converter                 #
# ########################################################################### #


def load_metadata(directoryPath: str) -> dict:
    """loads the metadata file in a python dictionary.

    args:
        directorypath (str): directory path to json file to load.

    raises:
        filenotfounderror: file [directorypath]/metadata.txt does not exist.
        exception: [directorypath]/metadata.txt is not readable by the user.
        jsondecodeerror: issue when loading the metadata from file.
    returns:
        dict: the loaded metadata.
    """
    metadata_file = directoryPath + "/metadata.txt"
    if not access(metadata_file, F_OK):
        raise FileNotFoundError(f"File {metadata_file} does not exists.")
    if not access(metadata_file, R_OK):
        raise Exception(f"File {metadata_file} is not readable for the user.")
    with open(file=metadata_file, mode="r") as file:
        metadata = json.load(file)
    return metadata


def load_dataframe(file_path):
    """loads a dataframe from a .csv file containing the audit data, creates one if none exist.

    args:
        directorypath (str): directory path to json file to load.

    raises:
        filenotfounderror: file [directorypath]/metadata.txt does not exist.
        exception: [directorypath]/metadata.txt is not readable by the user.
        jsondecodeerror: issue when loading the metadata from file.
    returns:
        dict: the loaded metadata.
    """
    if file_exists(file_path):
        df = pd.read_csv(file_path, index_col=False)
    else:
        df = pd.DataFrame(
            columns=[
                "URL",
                "expected_frames",
                "number_of_actual_frames",
                "expected_interval",
                "average_interval",
                "stdev_interval",
                "actual_length_seconds",
                "avg_fps",
            ]
        )
    return df


def audit_images(metadata: dict, directoryPath: str) -> dict:
    """Audits the video frames and saves the results to .csv file.

    Args:
        metadata: the metadata resulting from loadMetadata
        directoryPath: the directory where the images are located

    Returns:
        dict: a dictionary with the audited metadata
    """
    video_name = directoryPath.rsplit("/", 1)[-1]
    total_time_ms = 0
    expect_frame_no = 0
    expected_frames = metadata["Summary"]["Frames"]
    theoretical_interval = metadata["Summary"]["Interval_ms"]
    filenames_list = []
    intervals_list = []
    missing_frames = 0
    tmp_total_time_ms = 0

    for obj in metadata:
        if obj.startswith("Metadata-Default"):
            filename = obj.rsplit("/", 1)[-1]
            if filename != "Summary":
                cv_img = cv.imread(directoryPath + "/" + filename)
                if cv_img is None:
                    missing_frames += 1
                    expect_frame_no = expect_frame_no + 1
                    continue
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
                    missing_frames = missing_frames + 1

                # create a list of the intervals between two frames
                total_time_ms = metadata[obj]["ElapsedTime-ms"] - time_to_first_image
                intervals_list.append(total_time_ms - tmp_total_time_ms)
                tmp_total_time_ms = total_time_ms
                expect_frame_no = expect_frame_no + 1

    if expect_frame_no != expected_frames:
        missing_frames = expect_frame_no - expected_frames
    df = pd.DataFrame(intervals_list, columns=["intervals"])
    df2 = load_dataframe("/audit.csv")
    if video_name not in df2.values:
        df2.loc[len(df2.index)] = [
            video_name,
            expected_frames,
            expected_frames - missing_frames,
            theoretical_interval,
            df["intervals"].mean(),
            df["intervals"].std(),
            total_time_ms / 1000,
            expect_frame_no / (total_time_ms / 1000),
        ]
    else:
        df2.loc[df2["URL"] == video_name] = [
            video_name,
            expected_frames,
            expected_frames - missing_frames,
            theoretical_interval,
            df["intervals"].mean(),
            df["intervals"].std(),
            total_time_ms / 1000,
            expect_frame_no / (total_time_ms / 1000),
        ]
    df2.reset_index(drop=True, inplace=True)

    print(df2)
    df2.to_csv("./audit.csv", index=False)
    return {
        "number_of_expected_frames": expected_frames,
        "number_of_actual_frames": expected_frames - missing_frames,
        "expected_interval": theoretical_interval,
        "average_interval": df["intervals"].mean(),
        "stdev_interval": df["intervals"].std(),
        "actual_length_seconds": total_time_ms / 1000,
        "avg_fps": expect_frame_no / (total_time_ms / 1000),
    }
