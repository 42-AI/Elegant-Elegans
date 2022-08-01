import os
import stat
import sys
from ipaddress import summarize_address_range
from json import JSONDecodeError, dump

import pytest

sys.path.insert(1, os.path.join(sys.path[0], ".."))
from converter.parser import check_images, load_metadata


@pytest.fixture
def no_metadata_file(tmp_path):
    return tmp_path


@pytest.fixture
def random_metadata_file(tmp_path):
    dict_random = {
        "Lorem": {"ipsum": "dolor", "sit": "amet", "consectetur": "adipiscing", "elit": "In"},
        "bibendum": {
            "pharetra": "urna",
            "quis": "gravida",
            "Praesent": "pretium",
            "vitae": "augue",
        },
    }
    with open(tmp_path / "metadata.txt", "w") as file:
        dump(dict_random, file)
    return tmp_path


@pytest.fixture
def invalid_metadata_file(tmp_path):
    with open(tmp_path / "metadata.txt", "w") as file:
        file.write('Lorem" ipsum dolor sit amet consectetur adipiscing elit')
    return tmp_path


@pytest.fixture
def unreadable_metadata_file(tmp_path):
    with open(tmp_path / "metadata.txt", "w") as file:
        file.write('Lorem" ipsum dolor sit amet consectetur adipiscing elit')

    current = stat.S_IMODE(os.lstat(tmp_path / "metadata.txt").st_mode)
    os.chmod(tmp_path / "metadata.txt", current & ~stat.S_IEXEC)
    return tmp_path


@pytest.mark.parametrize(
    "metadata_path, expected",
    [
        ("random_metadata_file", "True"),
        ("no_metadata_file", FileNotFoundError(f"File metadata.txt does not exists.")),
        ("invalid_metadata_file", JSONDecodeError),
        ("unreadable_metadata_file", Exception),
    ],
)
def test_load_metadata(metadata_path, expected, request):
    """_summary_"""
    temporary_path = request.getfixturevalue(metadata_path)
    if isinstance(expected, (FileNotFoundError, JSONDecodeError, Exception)):
        with pytest.raises(Exception) as exception:
            load_metadata(str(temporary_path))
            assert exception.type == expected
    if expected is "True":
        return_dict = load_metadata(str(temporary_path))
        assert type(return_dict) == dict


# ============================================================================== #

test_dir = "test_tiffs/"
test_file = "img_channel000_position000_time000000011_z000.tif"


@pytest.fixture
def sync_test_repository_aws(test_id, tmp_path):
    """synchronize with different aws repository.

    Args:
        test_id (int): test id to try different possibility of correct/wrong directory

    Returns:
        str: string representing temporary directory
    Remarks:
        It could be simplify by one/two lines, but for readibility it is simpler like this.
    """
    if test_id == 1:
        # valid repository: exact number and name for image files
        os.system(f"aws s3 sync s3://lab-nematode/tests/test1 {tmp_path}")
        return str(tmp_path)
    elif test_id == 2:
        # invalid repository: 1 missing image in the middle
        os.system(f"aws s3 sync s3://lab-nematode/tests/test2 {tmp_path}")
        return str(tmp_path)
    elif test_id == 3:
        # invalid repository: invalid width and height of the 1st image
        os.system(f"aws s3 sync s3://lab-nematode/tests/test3 {tmp_path}")
        return str(tmp_path)
    elif test_id == 4:
        # invalid repository: number of image is not what it is expected
        os.system(f"aws s3 sync s3://lab-nematode/tests/test4 {tmp_path}")
        return str(tmp_path)


@pytest.mark.parametrize(
    "test_id, expected",
    [
        (1, "True"),
        (2, Exception),
        (3, Exception),
        (4, Exception),
    ],
)
def test_check_images(sync_test_repository_aws, expected):
    # synchronising with the corresponding test directory and retrieve the test directory
    directory = sync_test_repository_aws
    print("valeur de directory:", directory)
    print("contenue de directory:", os.listdir(directory))
    # Retrieving the metadata
    dict_metadata = load_metadata(directory)

    if isinstance(expected, (Exception, FileNotFoundError)):
        with pytest.raises(expected) as e:
            _ = check_images(dict_metadata, directory)
            assert e.type == expected
    if expected is "True":
        summarize_parsing_images = check_images(dict_metadata, directory)
        assert isinstance(summarize_parsing_images, dict)
