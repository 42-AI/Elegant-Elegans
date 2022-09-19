import json
import os


def extract_bucket_names(abs_file_path: str) -> list:
    """Extract aws bucket filepath from a txt file into a list.

    Does not take into account hashtag commented buckets.
    Args:
        abs_file_path (str): text file with the list of bucket path
    Returns:
        list: list of bucket paths
    """
    bucket_list = []
    with open(abs_file_path, "r") as f:
        while True:
            bucket_name = f.readline()
            if not bucket_name:
                break
            else:
                if bucket_name.find("#") == -1:
                    bucket_list.append(bucket_name.replace("\n", " "))
    return bucket_list


def load_metadata(directoryPath: str) -> dict:
    """loads the metadata file in a python dictionary.

    args:
        directorypath (str): directory path to json file to load.

    raises:
        filenotfounderror: file [directorypath]/metadata.txt does not exist.
        exception: [directorypath]/metadata.txt is not readable by the user.
        jsondecodeerror: issue when loading the metadata from file.
    returns:
        dict: the loaded metadata.
    """
    metadata_file = directoryPath + "/metadata.txt"
    if not os.access(metadata_file, os.F_OK):
        raise FileNotFoundError(f"File {metadata_file} does not exists.")
    if not os.access(metadata_file, os.R_OK):
        raise Exception(f"File {metadata_file} is not readable for the user.")
    with open(file=metadata_file, mode="r") as file:
        metadata = json.load(file)
    return metadata


def calculate_expected_fps(metadata_path=".") -> float:
    """Use the metadata file provided to retrieve a theoretical fps.

    Args:
        metadata_path (str, optional): path to the metadata file. Defaults to '.'.

    Returns:
        float: the number of theoretical fps retrieved from metadata
    """
    metadata = load_metadata(metadata_path)
    theoretical_interval = metadata["Summary"]["Interval_ms"]
    expected_fps = 1000 / theoretical_interval
    return expected_fps


def makeVideo(expected_fps: float, dir_name: str) -> None:
    """Use ffmpeg to make a video from available tif images in the provided dir.

    Args:
        expected_fps (float): fps used to make the video
        dir_name (str): name of dir containing tif images to convert
    """
    ffmpeg_cmd = "ffmpeg -loglevel 1 -framerate "
    ffmpeg_cmd += f"{expected_fps}"
    ffmpeg_cmd += f" -i img_channel000_position000_time%09d_z000.tif {dir_name}.mp4"
    print(ffmpeg_cmd)
    os.system(ffmpeg_cmd)


if __name__ == "__main__":
    working_dir = os.path.dirname(__file__)
    bucket_names_file = os.path.join(working_dir, "bucket_path.txt")
    bucket_list = extract_bucket_names(bucket_names_file)
    # Loop over each bucket to download images and convert them into a video
    for bucket_path in bucket_list:
        # Set up new dir and cd to it
        dir_name = (
            bucket_path.replace("/Default/", "")
            .replace("s3://lab-nematode/", "")
            .replace("/", "-")
            .replace(" ", "")
        )
        video_dir = os.path.join(working_dir, dir_name)
        if not os.path.exists(video_dir):
            os.mkdir(video_dir)
            os.chdir(video_dir)
            # Download all tiff images from an aws bucket
            aws_cmd = f"aws s3 cp {bucket_path} . --recursive"
            os.system(aws_cmd)
        else:
            raise FileExistsError(f"File {video_dir} already exists")
        # Create a video from previously downloaded images
        expected_fps = calculate_expected_fps()
        makeVideo(expected_fps, dir_name)
        os.chdir("../../../")
