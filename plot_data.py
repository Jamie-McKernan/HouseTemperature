import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt

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



df = pd.read_csv("./pi_data/zero.csv")

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
columns = ["temp", "x", "y"]
df = pd.DataFrame(geo_data, columns=columns)

# Plot
df = df.pivot_table("temp", "y", "x")


ax = sns.heatmap(
    df,
    # vmin=18,
    # vmax=24,
    cmap=sns.color_palette(
        "coolwarm",
        as_cmap=True
    )
)

ax.invert_yaxis()
ax.set_aspect("equal")

plt.axis("off")
plt.savefig(
    "test",
    dpi=170,
    facecolor=(0.55,0.55,0.55),
)