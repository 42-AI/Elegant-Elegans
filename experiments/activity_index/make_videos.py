import enum
import os


def extract_bucket_names(abs_file_path: str) -> list:
    """Extract aws bucket filepath from a txt file into a list.

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


if __name__ == "__main__":
    working_dir = os.path.dirname(__file__)
    bucket_names_file = os.path.join(working_dir, "bucket_path.txt")
    bucket_list = extract_bucket_names(bucket_names_file)
    for i, bucket_path in enumerate(bucket_list, start=1):
        # Set up new dir and cd to it
        dir_name = f"video_{i}"
        new_dir = os.path.join(working_dir, dir_name)
        os.mkdir(new_dir)
        os.chdir(new_dir)
        # Download all tiff images from an aws bucket
        aws_cmd = f"aws s3 cp {bucket_path} . --recursive"
        os.system(aws_cmd)
        # Create a video from previously downloaded images
        ffmpeg_cmd = "ffmpeg -loglevel 0 -framerate 33 -i "
        ffmpeg_cmd += f"img_channel000_position000_time%09d_z000.tif {dir_name}.mp4"
        os.system(ffmpeg_cmd)
        os.chdir("..")
