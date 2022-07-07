from datetime import datetime
import json
import cv2 as cv

#Some global vars to be replaced by out from args parser
interval = "Interval_ms"
summary = "Summary"

def loadMetadata(directoryPath):
    try:
        file_path = directoryPath + "/metadata.txt"
        metadata = json.load(open(file_path))
        return metadata
    except:
        raise Exception("Error trying to load metadata.txt")

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
        raise Exception("could not find start time in metadata file")

def loadTif(tifPath):
    cv_img = cv.imread(tifPath)
    return cv_img

def checkImages(metadata, directoryPath):
    total_time_ms = 0
    frames = 0
    expect_frame_no = 0
    expected_frames = metadata[summary]["Frames"]
    filenames = []

    for obj in metadata:
        if obj.startswith("Metadata-Default"):
            filename = obj.rsplit('/', 1)[-1]
            if filename != summary:

                cv_img = loadTif(directoryPath + "/" + filename)
                if cv_img is None:
                    raise Exception("Could not load file: " + directoryPath + "/" + filename)
                filenames.append(filename)
                actual_height, actual_width, layers = cv_img.shape
                expected_width, expected_height = metadata[obj]["Width"], metadata[obj]["Height"]
                if actual_height != expected_height or actual_width != expected_width:
                    raise Exception("Mismatched image size: frame: ", directoryPath + "/" + filename)
                
                currentFrame = metadata[obj]["Frame"]
                if currentFrame == 0:
                    time_to_first_image = metadata[obj]["ElapsedTime-ms"]
                    time_since_last_frame = 0
                else:
                    time_since_last_frame

                # checks for missing frames
                if currentFrame != expect_frame_no:
                    raise Exception("Mismatched frame number: expected frame no: ", expect_frame_no, " but got frame no: ", currentFrame)
                tmp = total_time_ms
                total_time_ms = metadata[obj]["ElapsedTime-ms"] - time_to_first_image
                time_since_last_frame = total_time_ms - tmp
                expect_frame_no = expect_frame_no + 1
                frames = frames + 1

    if frames == expected_frames:
        print("all expected frames were found")
        print("total capture time: ", total_time_ms)
        return {
            'avg_fps': frames / (total_time_ms / 1000),
            'frame_width': expected_width,
            'frame_height': expected_height,
            'frame_names': filenames,
        }
    return False
