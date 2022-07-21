import os
import sys
from os.path import exists

import pytest

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from converter.__main__ import main


@pytest.mark.parametrize(
    "video_name, format, expected",
    [
        ("elegans1", "avi", "elegans1.avi"),
        ("elegans2", "mp4", "elegans1.mp4"),
    ],
)
def test_video_creation(video_name, format, expected):
    test_dir = "test_tiffs/"
    os.system("aws s3 sync s3://lab-nematode/tests/test_1/ " + test_dir)
    os.system(f"python3 -m converter --path {test_dir} -o {video_name} -f {format}")
    assert exists(expected)
