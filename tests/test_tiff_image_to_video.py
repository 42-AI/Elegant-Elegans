import os
import sys
from pathlib import Path

import cv2
import pytest

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from converter.convert import tiff_images_to_video


class Test_convert:
    @pytest.mark.parametrize(
        "video_name, format, expected, exception_case",
        [
            ("vid0", "toto", ValueError, True),
            ("vid1", "avi", "vid1.avi", False),
            ("vid2", "mp4", "vid2.mp4", False),
            ("vid3.cd", "mp4", "vid3.cd.mp4", False),
        ],
    )
    def test_tiff_images_to_video(self, video_name, format, expected, exception_case):
        # SHOULD BE UPDATED WITH DIR_PATH TO TEST IMAGES
        dir_path = "imgs/"
        files = os.listdir(dir_path)
        frames = [f for f in files if f.endswith(".tif")]
        metadata = {
            "frame_names": sorted(frames),
            "frame_width": 2048,
            "frame_height": 2048,
            "avg_fps": 10,
        }
        if exception_case == True:
            with pytest.raises(Exception) as e:
                tiff_images_to_video(dir_path, video_name, format, metadata)
            assert e.type == expected
        else:
            path_to_file = expected
            tiff_images_to_video(dir_path, video_name, format, metadata)
            assert os.path.exists(path_to_file)
            vid_capture = cv2.VideoCapture(path_to_file)
            ret = vid_capture.isOpened()
            os.remove(path_to_file)
            assert ret
