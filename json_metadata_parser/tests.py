from curses import meta
from datetime import datetime
import json
from matplotlib.font_manager import json_load
import os
import re
from PIL import Image
from PIL.TiffTags import TAGS
from numpy import iinfo
import cv2 as cv


target_directory = "../data"


interval = "Interval_ms"
summary = "Summary"

def loadMetadata(directoryPath):
    try:
        file_path = directoryPath + "/metadata.txt"
        metadata = json_load(file_path)
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
                #TODO here it should throw an error if it does not find the tif file
                # cv_img = cv.imread(directoryPath + "/" + filename)

                cv_img = loadTif(directoryPath + "/" + filename)
                if cv_img is None:
                    print("could not load: ", directoryPath + "/" + filename, " aborting")
                    return
                actual_height, actual_width, layers = cv_img.shape
                # check if the size of the image matches the expected size from metadata file
                expected_width = metadata[obj]["Width"]
                expected_height = metadata[obj]["Height"]\

                if actual_height != expected_height or actual_width != expected_width:
                    print(".tif metadata mismatch")
                    return
                # TODO throw error if sizes don't match
                # checks for missing frames
                currentFrame = metadata[obj]["Frame"]
                if currentFrame == 0:
                    time_to_first_image = metadata[obj]["ElapsedTime-ms"]
                    time_since_last_frame = 0
                else:
                    time_since_last_frame
                if currentFrame != expect_frame_no:
                    print("THERE WAS AN ERROR")
                    break
                tmp = total_time_ms
                total_time_ms = metadata[obj]["ElapsedTime-ms"] - time_to_first_image
                time_since_last_frame = total_time_ms - tmp
                expect_frame_no = expect_frame_no + 1
                frames = frames + 1
            # print(time_since_last_frame)
            # print(meta_dict) #there may be some more info we want to check in img metadata
    if frames == expected_frames:
        print("all expected frames were found")
        print("total capture time: ", total_time_ms)

def main():
    metadata = loadMetadata("not_target_directory")
    metadata = loadMetadata(target_directory)
    checkImages(metadata, "not_target_directory")
    checkImages(metadata, target_directory)


if __name__=="__main__":
    main()
