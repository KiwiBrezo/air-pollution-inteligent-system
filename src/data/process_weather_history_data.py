import json
import os
from datetime import date

import pandas as pd

file_location = os.path.dirname(__file__)


def pre_preprocess_data_weather_historical():
    print("--- Started historical weather data pre-processing ---")

    csv_filename = os.path.join(file_location, "../../data/processed/processed_data_historical_weather.csv")
    raw_data_filename = os.path.join(file_location,
                                     "../../data/raw/weather/raw_data_" + date.today().strftime("%b-%d-%Y") + ".json")

    raw_file = open(raw_data_filename, "r+")

    data = json.load(raw_file)

    df = pd.DataFrame(
        columns=["datum_do", "temperature", "relativehumidity", "dewpoint", "surface_pressure", "cloudcover",
                 "windspeed", "winddirection"])

    df["datum_do"] = data["hourly"]["time"]
    df["temperature"] = data["hourly"]["temperature_2m"]
    df["relativehumidity"] = data["hourly"]["relativehumidity_2m"]
    df["dewpoint"] = data["hourly"]["dewpoint_2m"]
    df["surface_pressure"] = data["hourly"]["surface_pressure"]
    df["cloudcover"] = data["hourly"]["cloudcover"]
    df["windspeed"] = data["hourly"]["windspeed_10m"]
    df["winddirection"] = data["hourly"]["winddirection_10m"]

    df["datum_do"] = df["datum_do"].str.replace("T", " ")

    df.to_csv(csv_filename, index=False, header=True)

    print("     -> Done air pollution data pre-processing")


if __name__ == "__main__":
    pre_preprocess_data_weather_historical()