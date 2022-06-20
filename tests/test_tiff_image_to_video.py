from multiprocessing.sharedctypes import Value
import pytest
import os
import sys
from pathlib import Path

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from converter.tiff_image_to_video import tiff_images_to_video

@pytest.mark.parametrize(
    "video_name, format, expected, exception_case",
    [
        ("vid0", "toto", ValueError, True),
        ("vid1", "avi", "vid1.avi", False),
        ("vid2", "mp4", "vid2.mp4", False),
        ("vid3.cd", "mp4", "vid3.cd.mp4", False),
    ]
)
def test_tiff_images_to_video(video_name, format, expected, exception_case):
    dir_path = 'imgs/'
    if exception_case == True:
        with pytest.raises(Exception) as e:
            tiff_images_to_video(dir_path, video_name, format)
        assert e.type == expected
    else:
        tiff_images_to_video(dir_path, video_name, format)
        path_to_file = expected
        assert os.path.exists(path_to_file)
        os.remove(path_to_file)
