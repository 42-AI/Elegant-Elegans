import os
import sys

import pytest

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from converter.json_parser import check_images, load_metadata, load_tif

test_dir = "test_tiffs/"
test_file = "img_channel000_position000_time000000011_z000.tif"


@pytest.fixture
def get_first_tif_directory_test():
    os.system("aws s3 cp s3://lab-nematode/tests/test_1 . --recursive")
    return "test_1/"


@pytest.fixture
def get_second_tif_directory_test():
    os.system("aws s3 cp s3://lab-nematode/tests/test_2 . --recursive")
    return "test_2/"


@pytest.fixture
def get_third_tif_directory_test():
    os.system("aws s3 cp s3://lab-nematode/tests/test_3 . --recursive")
    return "test_3/"


@pytest.fixture
def get_fourth_tif_directory_test():
    os.system("aws s3 cp s3://lab-nematode/tests/test_4 . --recursive")
    return "test_4/"


# When using fixture, it allows to create temporary variable and repository which will exist only within the tests.
# Thus, doing aws s3 cp/sync will download the repository from aws s3 during the test and delete them after.
@pytest.mark.parametrize(
    "input, expected",
    [
        "get_first_tif_directory_test",
        "status_ok",
        "get_second_tif_directory_test",
        "status_false",
        "get_third_tif_directory_test",
        "status_false",
        "get_fourth_tif_directory_test",
        "status_false",
    ],
)
def test_load_metadata(input, expected, request):
    request.getfixturevalue(input)
    metadata = load_metadata(test_dir)
    assert type(metadata) == dict


def test_missing_file():
    os.system("aws s3 sync s3://lab-nematode/tests/test_1/ " + test_dir)
    new_name = "new_name"
    os.rename(test_dir + test_file, test_dir + new_name)
    try:
        check_images(load_metadata(test_dir), test_dir)
    except Exception:
        os.rename(test_dir + new_name, test_dir + test_file)
        assert True


def test_missing_framecount():
    os.system("aws s3 sync s3://lab-nematode/tests/test_1/ " + test_dir)
    metadata = load_metadata(test_dir)
    del metadata["Summary"]["Frames"]
    try:
        output_dict = check_images(metadata, test_dir)
    except:
        assert True


def test_wrong_width():
    import json

    os.system("aws s3 sync s3://lab-nematode/tests/test_1/ " + test_dir)
    metadata = load_metadata(test_dir)
    metadata["Metadata-Default/" + test_file]["Width"] -= 1
    with open(test_dir + "metadata.txt", "w") as outfile:
        json.dump(metadata, outfile)
    try:
        check_images(load_metadata(test_dir), test_dir)
        assert False
    except Exception:
        assert True


def test_wrong_height():
    import json

    os.system("aws s3 sync s3://lab-nematode/tests/test_1/ " + test_dir)
    metadata = load_metadata(test_dir)
    metadata["Metadata-Default/" + test_file]["Height"] -= 1
    with open(test_dir + "metadata.json", "w") as outfile:
        json.dump(metadata, outfile)
    try:
        check_images(load_metadata(test_dir), test_dir)
        assert False
    except Exception:
        assert True


def test_output_format():
    os.system("aws s3 sync s3://lab-nematode/tests/test_1/ " + test_dir)
    output_dict = check_images(load_metadata(test_dir), test_dir)
    assert "avg_fps" in output_dict
    assert "frame_width" in output_dict
    assert "frame_height" in output_dict
    assert "frame_names" in output_dict
