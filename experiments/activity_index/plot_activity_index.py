import os
import re

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def extract_data_from_directory(dir: str) -> pd.DataFrame:
    """Extract data from each particles.csv file found in 'results' dir
       and stack it in a single dataframe
       The data is linked to each video results with the column 'dataset_name'
    Args:
        dir (str): dir containing the data for each video analyzed

    Returns:
        pd.DataFrame: all the data extracted and stacked from particles.csv files
    """
    pwd = os.path.dirname(__file__)
    result_dir = os.path.join(pwd, dir)
    list_subdir = os.listdir(result_dir)
    results_subdir = [d for d in list_subdir if os.path.isdir(os.path.join(result_dir, d))]
    files = [
        f
        for d in results_subdir
        for f in os.listdir(os.path.join(pwd, dir, d))
        if f.endswith(".csv")
    ]
    data = pd.DataFrame()
    for subdir, file in zip(results_subdir, files):
        file_path = os.path.join(pwd, dir, subdir, file)
        id_num = re.findall("[0-9]+", subdir)[0]
        name = f"results_{id_num}"
        if os.path.isfile(file_path):
            data_subset = pd.read_csv(file_path, index_col=0)
            data_subset = data_subset.assign(dataset_name=name)
            if data.empty:
                data = data_subset
            else:
                data = pd.concat([data, data_subset], ignore_index=True)
    return data


def cleaning_data(data: pd.DataFrame) -> pd.DataFrame:
    data = data.dropna(axis=1, how="all")
    return data


if __name__ == "__main__":
    raw_data = extract_data_from_directory("results")
    cleaned_data = cleaning_data(raw_data)
    data = cleaned_data[["Activity Index", "BPM", "Area", "Eccentricity", "dataset_name"]].copy()
    # Remove all rows with an activity index that is null
    data = data[data["Activity Index"] != 0]
    try:
        sns.displot(
            data=data, x=data["Activity Index"], hue="dataset_name", multiple="stack", bins=20
        )
        plt.show()
    except:
        print("ERROR: cannot plot your data")
