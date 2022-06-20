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
from datetime import datetime
import json
import cv2 as cv

#Some global vars to be replaced by out from args parser
interval = "Interval_ms"
summary = "Summary"

def parser() -> dict:
    """
        Parse arguments to get name directory as input and the video file's
        name as output
    Return:
    -------
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
        "--output", type=str, required=True, help="Name of the converted video."
    )
    return parser.parse_args()

def loadMetadata(directoryPath):
    try:
        file_path = directoryPath + "/metadata.txt"
        metadata = json.load(open(file_path))
        return metadata
    except:
        print("Error trying to load metadata.txt")


def padMicroSecs(timestamp):
    parts = timestamp.split('.')
    return '.'.join(parts[:-1] + ['{:06d}'.format(int(parts[-1]))])

def getStartTime(metadata):
    try:
        strTime = metadata[summary]["StartTime"]
        strTime_without_timezone = strTime[:-6]
        #TODO need to double check here that i'm doing the right thing with the padding
        strTime_without_timezone = padMicroSecs(strTime_without_timezone)
        start_time = datetime.strptime(strTime_without_timezone, "%Y-%m-%d %H:%M:%S.%f")
        return start_time
    except:
        print("could not find start time in metadata file")

def loadTif(tifPath):
    cv_img = cv.imread(tifPath)
    return cv_img

def checkImages(metadata, directoryPath):
    total_time_ms = 0
    frames = 0
    expect_frame_no = 0
    expected_frames = metadata[summary]["Frames"]


    for obj in metadata:
        if obj.startswith("Metadata-Default"):
            filename = obj.rsplit('/', 1)[-1]
            if filename != summary:

                cv_img = loadTif(directoryPath + "/" + filename)
                if cv_img is None:
                    raise Exception("File not found")
                    #print("could not load: ", directoryPath + "/" + filename, " aborting")
                    #return

                actual_height, actual_width, layers = cv_img.shape
                expected_width, expected_height = metadata[obj]["Width"], metadata[obj]["Height"]
                if actual_height != expected_height or actual_width != expected_width:
                    raise Exception("Mismatched dimensions")
                    #print(".tif metadata mismatch on frame: ", directoryPath + "/" + filename, " aborting")
                    #return
                
                currentFrame = metadata[obj]["Frame"]
                if currentFrame == 0:
                    time_to_first_image = metadata[obj]["ElapsedTime-ms"]
                    time_since_last_frame = 0
                else:
                    time_since_last_frame

                # checks for missing frames
                if currentFrame != expect_frame_no:
                    raise Exception("Mismatched frame number")
                    #print("expected frame no: ", expect_frame_no, " but got frame no: ", currentFrame, " check for missing frames")
                    #break
                tmp = total_time_ms
                total_time_ms = metadata[obj]["ElapsedTime-ms"] - time_to_first_image
                time_since_last_frame = total_time_ms - tmp
                expect_frame_no = expect_frame_no + 1
                frames = frames + 1

    if frames == expected_frames:
        print("all expected frames were found")
        print("total capture time: ", total_time_ms)
        return True
    return False

# ########################################################################## #
#                                   MAIN                                     #
# ########################################################################## #

if __name__=="__main__":
    args = parser()

    # print(args)
    dir_path = args.path
    metadata = loadMetadata(dir_path)
    checkImages(metadata, dir_path)