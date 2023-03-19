import os
import urllib.request
from datetime import date

import pandas as pd

file_location = os.path.dirname(__file__)


def get_data_weather_history():
    air_pollution_csv_filename = os.path.join(file_location, "../../data/processed/processed_data_air_pollution.csv")
    df_air_pollution = pd.read_csv(air_pollution_csv_filename)

    min_date = min(df_air_pollution["datum_do"])
    max_date = max(df_air_pollution["datum_do"])

    min_date = pd.to_datetime(min_date).date().strftime("%Y-%m-%d")
    max_date = pd.to_datetime(max_date).date().strftime("%Y-%m-%d")

    url = "https://archive-api.open-meteo.com/v1/archive?latitude=46.42&longitude=15.87&start_date=" + min_date + "&end_date=" + max_date + "&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,surface_pressure,cloudcover,windspeed_10m,winddirection_10m&timezone=Europe%2FBerlin"

    print("--- Started download historical weather raw data ---")
    print("     -> Getting data from: ", url)
    with urllib.request.urlopen(url) as response:
        raw_data_filename = os.path.join(file_location, "../../data/raw/weather/raw_data_" + date.today().strftime(
            "%b-%d-%Y") + ".json")
        raw_file = open(raw_data_filename, "wb+")

        print("     -> Done download, saving to file...")

        raw_file.write(response.read())
        raw_file.close()

        print("     -> Done saving to file")


if __name__ == "__main__":
    get_data_weather_history()