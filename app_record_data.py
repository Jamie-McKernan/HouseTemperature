import csv
import time
import pause
import datetime as dt
import statistics as stat

from random import randint


def get_temp():
    return (randint(1800, 2500)/100)


def get_data_sample(data_samples_for_average):

    # reset data to empty lists
    for key in data_samples_for_average.keys():
        data_samples_for_average[key] = []

    for _ in range(10):
        data_samples_for_average["temp"].append(get_temp())
        print("getting temp data")
        time.sleep(1)

    return_data = {}

    for data_type, values in data_samples_for_average.items():
        return_data[data_type] = round(stat.mean(values), 2)

    return return_data


def record_data():

    # static list of data types to record
    all_data_names = {
        "temp": []
    }

    # create csv header list
    static_fieldnames = ["time", "piid"]
    fieldnames = [key for key in all_data_names.keys()]
    fieldnames += static_fieldnames

    with open("current_piid.txt", 'r') as piid_file:
        piid = piid_file.read()

    with open(f"{piid}.csv", 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

    now = dt.datetime.now()
    now_adjusted = now.replace(microsecond=0, second=0)
    next_minute = now_adjusted + dt.timedelta(0, 60)
    pause.until(next_minute)

    while True:
        now = dt.datetime.now()
        now_adjusted = now.replace(microsecond=0, second=0)
        next_minute = now_adjusted + dt.timedelta(0, 60)

        time_string = f"{str(now_adjusted.hour).zfill(2)}{str(now_adjusted.minute).zfill(2)}"
        print("getting data sample")
        data_sample = get_data_sample(all_data_names)
        data_sample["piid"] = piid
        data_sample["time"] = time_string
        print("got data sample, now writing...")
        with open(f"{piid}.csv", 'a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow(data_sample)

        pause.until(next_minute)

record_data()