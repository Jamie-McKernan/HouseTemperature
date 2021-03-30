import os
import datetime
import csv
import random

import progressbar
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt

from multiprocessing import Pool
from random import randint

from matplotlib.colors import LinearSegmentedColormap

# my_cmap = LinearSegmentedColormap.from_list('mycmap', [(0,0,1), (1,1,1), (1,0,0)])


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

DATA_FOLDER = "./data"
IMAGE_OUTPUT_FOLDER = "./images"
os.system(f"mkdir {IMAGE_OUTPUT_FOLDER}")
os.system(f"mkdir outputs")

def plot_single_time(args):
    df, time_string, min_temp, max_temp, img_number, data_metric = args

    geo_data = []

    # Add CSV data to list
    for index, row in df.iterrows():
        for coord_set in PI_LOCATIONS[row["piid"]]:
            geo_data.append((
                row["rolling"],
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
        vmin=float(min_temp),
        vmax=float(max_temp),
        # cmap=my_cmap
        cmap=sns.color_palette(
            # "coolwarm",
            "magma",
            as_cmap=True
        ),
        # annot=True
    )


    plt.title(
        f"{data_metric} -- {time_string[0:2]}:{time_string[2:]}",
        # y=1.3,
        fontsize=23,
        color="white"
    )

    ax.invert_yaxis()
    ax.set_aspect("equal")

    cax = plt.gcf().axes[-1]
    cax.tick_params(labelsize=10, labelcolor="white", color="white")

    plt.axis("off")
    plt.savefig(
        (
            f"{IMAGE_OUTPUT_FOLDER}/"
            f"{data_metric.replace('(', '_').replace(')', '')}/"
            f"{img_number}"
        ),
        dpi=200,
        facecolor=(0.5,0.5,0.5),
    )
    plt.clf()
    return


def sort_all_data(data_type="temp(c)", rolling_window=1):
    all_time_loc_data = []

    for csv_file in os.listdir(DATA_FOLDER):
        with open(f"{DATA_FOLDER}/{csv_file}", 'r') as read_obj:
            csv_reader = csv.DictReader(read_obj)
            one_loc_data = [[row["piid"], row["time"], float(row[data_type])] for row in csv_reader]

        all_time_loc_data += one_loc_data

    df_all_data = pd.DataFrame(
        all_time_loc_data,
        columns=["piid", "time", "temp"]
    )

    df_all_data["rolling"] = df_all_data["temp"].rolling(window=rolling_window).mean()
    return df_all_data


def plot_all_data(df_all_data, data_metric="temp(c)"):
    
    os.system(f"mkdir ./{IMAGE_OUTPUT_FOLDER}/{data_metric.replace('(', '_').replace(')', '')}")

    min_temp = df_all_data["temp"].min()
    max_temp = df_all_data["temp"].max()

    widgets = [
        progressbar.Timer(format="%(elapsed)s"),
        progressbar.Percentage(),
        progressbar.Bar(marker="\x1b[32m█\x1b[39m"),
        progressbar.ETA()
    ]

    list_of_arg_lists = []
    # for count, time_value in enumerate(progressbar.progressbar(df_all_data.time.unique(), widgets=widgets)):
    for count, time_value in enumerate(df_all_data.time.unique()):

        df_single_time = df_all_data.loc[
            df_all_data["time"] == time_value
        ]

        list_of_arg_lists.append([
            df_single_time,
            time_value,
            min_temp,
            max_temp,
            count,
            data_metric
        ])

        # plot_single_time([
        #     df_single_time,
        #     time_value,
        #     min_temp,
        #     max_temp,
        #     count
        # ])

    with Pool(processes=8) as pool:
        r = list(
            progressbar.progressbar(
                pool.imap(
                    plot_single_time,
                    list_of_arg_lists
                ), 
                widgets=widgets, 
                max_value=len(list_of_arg_lists)
            )
        )


def random_data():

    time_list = []

    for i in range(24):
        for j in range(60):
            time_list.append(f"{str(i).zfill(2)}{str(j).zfill(2)}")

    piid_list = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine"
    ]

    random_data_list = []
    
    random_constant = float(23)


    for piid in piid_list:
        continuous_value = False
        add_or_remove = random.choice([[-1, -1, -1, 1, 1, 1, 1, 1], [-1, -1, -1, -1, -1, 1, 1, 1]])
        for time in time_list:
            if not continuous_value:
                continuous_value = \
                    random_constant + (random.choice(add_or_remove) * (randint(1, 50)/100))
            else:
                continuous_value += (random.choice(add_or_remove) * (randint(1, 50)/100))


            random_data_list.append(
                [piid, str(time), continuous_value]
            )

    random_df = pd.DataFrame(
        random_data_list,
        columns=["piid", "time", "temp"]
    )

    random_df["rolling"] = random_df["temp"].rolling(window=15).mean()

    return random_df


def make_video(framerate, filename="video", data_metric="temp(c)"):
    format_string = r"%01d"

    filename = filename.replace("(", "_").replace(")", "")

    os.system(
        f'ffmpeg -framerate {framerate} -i "./images/{filename}/{format_string}.png" -vcodec libx264 -pix_fmt yuv420p ./outputs/{filename}.mp4'
    )
    return



### Other Values

# temp(c)
# pressure(hPa) (earth is 985 on average)
# humidity(percent)
# light(lux)

### Other Values



DM_LIST = [
    "temp(c)",
    "pressure(hPa)",
    "humidity(percent)",
    "light(lux)"
]

# DATA_METRIC = "light(lux)"

for DATA_METRIC in DM_LIST:

    ### Real data
    all_data_sorted = sort_all_data(
        data_type=DATA_METRIC,
        rolling_window=15
    )
    plot_all_data(all_data_sorted, DATA_METRIC)


    ### Random data
    # random_df = random_data()
    # plot_all_data(random_df, "temp(c)")

    make_video(30, DATA_METRIC)
