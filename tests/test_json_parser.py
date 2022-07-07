import pytest
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from converter.json_parser import loadMetadata, loadTif, checkImages

test_dir = "test_tiffs/"
test_file = "img_channel000_position000_time000000011_z000.tif"

def test_load_metadata():
    os.system("aws s3 sync s3://lab-nematode/tests/test_1/ " + test_dir)
    metadata = loadMetadata(test_dir)
    assert type(metadata) == dict

def test_missing_file():
    os.system("aws s3 sync s3://lab-nematode/tests/test_1/ " + test_dir)
    new_name = "new_name"
    os.rename(test_dir + test_file, test_dir + new_name)
    try:
        checkImages(loadMetadata(test_dir), test_dir)
    except Exception:
        os.rename(test_dir + new_name, test_dir + test_file)
        assert True

def test_missing_framecount():
    os.system("aws s3 sync s3://lab-nematode/tests/test_1/ " + test_dir)
    metadata = loadMetadata(test_dir)
    del metadata["Summary"]["Frames"]
    try:
        output_dict = checkImages(metadata, test_dir)
    except:
        assert True

def test_wrong_width():
    import json
    os.system("aws s3 sync s3://lab-nematode/tests/test_1/ " + test_dir)
    metadata = loadMetadata(test_dir)
    metadata['Metadata-Default/'+ test_file]['Width'] -= 1
    with open(test_dir+'metadata.txt', 'w') as outfile:
        json.dump(metadata, outfile)
    try:
        checkImages(loadMetadata(test_dir), test_dir)
        assert False
    except Exception:
        assert True

def test_wrong_height():
    import json
    os.system("aws s3 sync s3://lab-nematode/tests/test_1/ " + test_dir)
    metadata = loadMetadata(test_dir)
    metadata['Metadata-Default/'+ test_file]['Height'] -= 1
    with open(test_dir+'metadata.json', 'w') as outfile:
        json.dump(metadata, outfile)
    try:
        checkImages(loadMetadata(test_dir), test_dir)
        assert False
    except Exception:
        assert True

def test_output_format():
    os.system("aws s3 sync s3://lab-nematode/tests/test_1/ " + test_dir)
    output_dict = checkImages(loadMetadata(test_dir), test_dir)
    assert 'avg_fps' in output_dict
    assert 'frame_width' in output_dict
    assert 'frame_height' in output_dict
    assert 'frame_names' in output_dict
