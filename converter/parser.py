import argparse


# Parser related to the arguments of converter program
def parser() -> dict:
    """Parse arguments to get name directory as input and the video file's name as output.

    Return:
        A dictionary containing the name of the path to input directory
        and the defined name of the video file as output
        Namespace(output='', path='')
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path", type=str, required=True, help="path where source will be look in."
    )
    parser.add_argument(
        "-o", "--output", type=str, required=True, help="Name of the converted video."
    )
    return parser.parse_args()
