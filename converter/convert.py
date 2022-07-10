import os
from importlib.metadata import metadata

import cv2


def select_video_compression_format(format):
    """Select the right compression codec to be passed to VideoWriter
    Args:
        format (string): format use for video compression

    Raises:
        ValueError: raise an error if an unknown format is passed

    Returns:
        int: fourcc identifier
        Four-character codec (fourcc) describes which
        codec is used to compress the video
    """
    if format == "mp4":
        video_compression = cv2.VideoWriter_fourcc(*"mp4v")
    elif format == "avi":
        video_compression = cv2.VideoWriter_fourcc(*"FMP4")
    else:
        raise ValueError(f"{format} not supported.")
    return video_compression


def tiff_images_to_video(dir_path, video_name, format, metadata):
    """Create a video file in the current directory from a set of tif images.

    Args:
        dir_path (string): directory path to tiff images to convert
        video_name (string, optional): radical of the video filename.
                                       Defaults to None.
        format (string): compression format for the final video
        metadata (dict): contains a list of file_names in ascending
                         order, the average fps, the frame width and
                         the frame height
    """

    # Prepare several parameters for VideoWriter
    codec = select_video_compression_format(format)
    fps = metadata.get("avg_fps")
    width = metadata.get("frame_width")
    height = metadata.get("frame_height")
    frame_size = (width, height)
    # Initialize video
    output_name = video_name + "." + format
    video = cv2.VideoWriter(output_name, codec, fps, frame_size)

    # Loop through each image and add them to the VideoWriter object
    frames_list = metadata.get("frame_names")
    for file_name in frames_list:
        img = cv2.VideoCapture(dir_path + file_name)
        ret, frame = img.read()
        if ret:
            video.write(frame)
        else:
            raise RuntimeError(f"Input image corrupted - {file_name}")
    video.release()
