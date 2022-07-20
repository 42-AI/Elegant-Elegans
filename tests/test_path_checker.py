import os
import sys

import pytest

sys.path.insert(1, os.path.join(sys.path[0], ".."))

import shutil

from converter.__main__ import path_checker, path_inside_checker


def create_repertories():
    test1 = os.path.join(os.getcwd(), "test1")
    if not os.path.exists(test1):
        os.makedirs(test1)


@pytest.mark.parametrize(
    "path, expected",
    [
        (os.getcwd(), None),
    ],
)
def test_path_checker(path: str, expected: str):
    assert path_checker(path) == expected, "All good !"


@pytest.mark.parametrize(
    "path, expected, message",
    [
        ("toto", NotADirectoryError, "toto is not a directory."),
    ],
)
def test_path_checker_directory(path: str, expected, message: str):
    with pytest.raises(expected) as e:
        path_checker(path)
    assert (message) in str(e.value)
    assert e.type == expected


@pytest.mark.parametrize(
    "path, expected, message",
    [
        ("koko", PermissionError, "Permission denied to koko"),
    ],
)
def test_path_permission(path: str, expected, message: str):
    os.mkdir(os.path.join(os.getcwd(), path), 0o000)
    with pytest.raises(expected) as e:
        path_checker(path)
    assert (message) in str(e.value)
    assert e.type == expected
    os.rmdir(os.path.join(os.getcwd(), path))


def create_repertories(dir_path: str):
    test1 = os.path.join(os.getcwd(), dir_path)
    os.mkdir(test1)


def f_case1(dir_path: str):
    name_of_file = "random"
    random = os.path.join(dir_path, name_of_file + ".txt")
    file_txt = open(random, "w")


def f_case2(dir_path: str):
    name_of_file = "random"
    random = os.path.join(dir_path, name_of_file + ".tiff")
    file_txt = open(random, "w")


def f_case3(dir_path: str):
    name_of_file = "random"
    random = os.path.join(dir_path, name_of_file)
    file_txt = open(random + ".json", "w")
    file_txt2 = open(random + "2.json", "w")


def f_case4(dir_path: str):
    name_of_file = "random"
    random = os.path.join(dir_path, name_of_file)
    file_txt = open(random + ".tiff", "w")
    file_txt2 = open(random + ".json", "w")
    pass


dct_cases = [f_case1, f_case2, f_case3, f_case4]


@pytest.mark.parametrize(
    "id_test, dir_path, message",
    [
        (0, "test1", "File other than .tiff or .json found"),
        (1, "test2", "No .json file found"),
        (2, "test3", "More than one .json file found"),
        (3, "test4", "Number of .tiff files insufficient (min required 100)"),
    ],
)
def test_path_inside_checker(id_test: int, dir_path: str, message: str):
    create_repertories(dir_path)
    dct_cases[id_test](dir_path)
    path = os.path.join(os.getcwd(), dir_path)
    with pytest.raises(Exception) as e:
        path_inside_checker(path)
    assert (message) in str(e.value)
    assert e.type == Exception

    shutil.rmtree(dir_path)
