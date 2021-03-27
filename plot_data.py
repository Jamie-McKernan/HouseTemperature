import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt

from csv import reader


# Constants
COORDS = {
    "hallway": [(1, 2), (2, 2)],
    "utility_room": [(1, 4), (2, 4)],
    "kitchen": [(1, 5), (2, 5)],
    "small_cupboard": [(2, 1)],
    "parents_bedroom": [
        (3, 1),
        (3, 2),
        (4, 1),
        (4, 2),
        (5, 1),
        (5, 2),
    ],
    "living_room": [
        (3, 3),
        (3, 4),
        (4, 3),
        (4, 4),
        (5, 3),
        (5, 4),
    ],
    "dining_area": [
        (3, 5),
        (4, 5),
        (5, 5),
    ],
    "my_bedroom": [
        (8, 3),
        (8, 4),
        (9, 3),
        (9, 4),
        (10, 3),
        (10, 4),
    ],
    "cam_bedroom": [
        (9, 1),
        (9, 2),
        (10, 1),
        (10, 2),
    ],
    "office": [
        (6, 3),
        (6, 4),
        (7, 3),
        (7, 4),
    ],
}

PI_LOCATIONS = {
    "zero": COORDS["hallway"],
    "one": COORDS["small_cupboard"],
    "two": COORDS["parents_bedroom"],
    "three": COORDS["living_room"],
    "four": COORDS["dining_area"],
    "five": COORDS["utility_room"],
    "six": COORDS["kitchen"],
    "seven": COORDS["office"],
    "eight": COORDS["my_bedroom"],
    "nine": COORDS["cam_bedroom"]
}

DATA_FOLDER = "./pi_data_raw"
IMAGE_OUTPUT_FOLDER = "./images"



def plot_single_time(df, time_string):
    geo_data = []

    # Add CSV data to list
    for index, row in df.iterrows():
        for coord_set in PI_LOCATIONS[row["piid"]]:
            geo_data.append((
                row["temp"],
                coord_set[0],
                coord_set[1]
            ))

    # Make DataFrame from list
    df = pd.DataFrame(geo_data, columns=["temp", "x", "y"])

    df = df.astype("float")

    # Plot
    df = df.pivot_table("temp", "y", "x")


    ax = sns.heatmap(
        df,
        vmin=18,
        vmax=24,
        cmap=sns.color_palette(
            "coolwarm",
            as_cmap=True
        )
    )

    plt.title(
        f"{time_string[0:1]}:{time_string[2:]}",
        y=1.3,
        fontsize=23,
        color="white"
    )

    ax.invert_yaxis()
    ax.set_aspect("equal")

    cax = plt.gcf().axes[-1]
    cax.tick_params(labelsize=10, labelcolor="white", color="white")

    plt.axis("off")
    plt.savefig(
        f"{IMAGE_OUTPUT_FOLDER}/{time_string}",
        dpi=170,
        facecolor=(0.5,0.5,0.5),
    )
    plt.clf()


def plot_all_data():
    all_time_loc_data = []

    for csv_file in os.listdir(DATA_FOLDER):
        with open(f"{DATA_FOLDER}/{csv_file}", 'r') as read_obj:
            csv_reader = reader(read_obj)
            header = next(csv_reader)
            one_loc_data = [row for row in csv_reader]
        all_time_loc_data += one_loc_data

    df_all_data = pd.DataFrame(
        all_time_loc_data,
        columns=["piid", "time", "temp"]
    )

    for time_value in df_all_data.time.unique():
        df_single_time = df_all_data.loc[
            df_all_data["time"] == time_value
        ]

        plot_single_time(df_single_time, time_value)


plot_all_data()