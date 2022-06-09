import cv2
import numpy as np
import os


def select_video_compression_format(format):
    """Select the right compression identifier to be passed to VideoWriter

    Args:
        format (string): format use for video compression

    Raises:
        ValueError: raise an error if an unknown format is passed

    Returns:
        int: fourcc identifier
    """
    # Four-character codec (fourcc) describes
    # which format is used to compress the video
    if format == "mp4":
        video_compression = cv2.VideoWriter_fourcc(*'mp4v')
    elif format == "avi":
        video_compression = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    else:
        raise ValueError(f"{format} not supported.")
    return video_compression


def tiff_images_to_video(dir_path, format, video_name=None):
    """Create a video file in the current directory from a set of tif images

    Args:
        dir_path (string): directory path of the tif images to convert
        format (string): compression format for the final video
        video_name (string, optional): radical of the video filename. Defaults to None.
    """
    # Store all files from a dir_path in an list and sort file in ascending order
    file_listing = os.listdir(dir_path)
    sorted_file_listing = sorted(file_listing)

    # Prepare several args for VideoWriter
    video_compression = select_video_compression_format(format)
    fps = 25
    frame_size = (2048, 2048)
    video_name = video_name if video_name is not None else dir_path
    
    # Define parameter used for VideoWriter
    video = cv2.VideoWriter(video_name + '.' + format, video_compression, fps, frame_size)

    # Loop through each image and add them to the VideoWriter object
    for file_name in sorted_file_listing:
        if file_name.endswith(".tif"):
            img = cv2.VideoCapture(dir_path + file_name)
            ret, frame = img.read()
            video.write(frame)
    video.release()

# Before launch:
# > mkdir imgs
# > cd imgs
# > aws s3 cp s3://BUCKET/FOLDER . --recursive
# Change the path
if __name__ == '__main__':
    format = 'avi'
    # format = 'mp4'
    dir_path = 'imgs/'
    video_name = "vid1"
    tiff_images_to_video(dir_path, format, video_name)