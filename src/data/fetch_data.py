import os
import json
import urllib.request

import pandas as pd
from datetime import date

file_location = os.path.dirname(__file__)


def get_data_air_pollution():
    url = "https://arsoxmlwrapper.app.grega.xyz/api/air/archive"

    print("--- Started download air pollution raw data ---")
    print("     -> Getting data from: ", url)
    with urllib.request.urlopen(url) as response:
        raw_data_filename = os.path.join(file_location,
                                         "../../data/raw/air/raw_data_" + date.today().strftime("%b-%d-%Y") + ".json")
        raw_file = open(raw_data_filename, "wb")

        print("     -> Done download, saving to file...")

        raw_file.write(response.read())
        raw_file.close()

        print("     -> Done saving to file")


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
        raw_file = open(raw_data_filename, "wb")

        print("     -> Done download, saving to file...")

        raw_file.write(response.read())
        raw_file.close()

        print("     -> Done saving to file")


def pre_preprocess_data_air_pollution():
    print("--- Started air pollution data pre-processing ---")

    csv_filename = os.path.join(file_location, "../../data/processed/processed_data_air_pollution.csv")
    raw_data_filename = os.path.join(file_location,
                                     "../../data/raw/air/raw_data_" + date.today().strftime("%b-%d-%Y") + ".json")
    raw_file = open(raw_data_filename, "r")

    data = json.load(raw_file)
    meteoroloske_data = []

    for item in data:
        item_json = json.loads(item["json"])
        item_arr_postaj = item_json["arsopodatki"]["postaja"]
        item_postaja_data = [x for x in item_arr_postaj if x["merilno_mesto"] == "Ptuj"]

        meteoroloske_data.append(item_postaja_data[0])

    lst = [[x["datum_do"], x["ge_dolzina"], x["ge_sirina"], x["merilno_mesto"], x["nadm_visina"], x["pm2.5"], x["pm10"],
            x["sifra"]] for x in meteoroloske_data]
    df = pd.DataFrame(lst,
                      columns=["datum_do", "ge_dolzina", "ge_sirina", "merilno_mesto", "nadm_visina", "pm25", "pm10",
                               "sifra"])
    df.to_csv(csv_filename, index=False, header=True)

    print("     -> Done air pollution data pre-processing")


def pre_preprocess_data_weather_historical():
    print("--- Started historical weather data pre-processing ---")

    csv_filename = os.path.join(file_location, "../../data/processed/processed_data_historical_weather.csv")
    raw_data_filename = os.path.join(file_location,
                                     "../../data/raw/weather/raw_data_" + date.today().strftime("%b-%d-%Y") + ".json")

    raw_file = open(raw_data_filename, "r")

    data = json.load(raw_file)

    df = pd.DataFrame(
        columns=["datum_do", "temperature", "relativehumidity", "dewpoint", "dewpoint", "surface_pressure", "cloudcover",
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


def merge_processed_data():
    print("--- Started margin data ---")

    air_pollution_csv_filename = os.path.join(file_location, "../../data/processed/processed_data_air_pollution.csv")
    historical_weather_csv_filename = os.path.join(file_location, "../../data/processed/processed_data_historical_weather.csv")
    merged_csv_filename = os.path.join(file_location, "../../data/processed/processed_data_merged.csv")

    df_air_pollution = pd.read_csv(air_pollution_csv_filename)
    df_historical_weather = pd.read_csv(historical_weather_csv_filename)

    df_air_pollution = df_air_pollution.sort_values("datum_do")
    df_historical_weather = df_historical_weather.sort_values("datum_do")

    df_merged = df_historical_weather.merge(df_air_pollution, how="outer").sort_values("datum_do")

    number_of_rows_before = len(df_merged.index)

    #Odstranimo vse vrstice v katerih se pojavi podatek NaN
    df_merged = df_merged.dropna()

    number_of_rows_after = len(df_merged.index)

    print("     -> Marged dataframe was reduced by", number_of_rows_before - number_of_rows_after, "rows")

    df_merged.to_csv(merged_csv_filename, index=False, header=True)

    print("     -> Done margin data")


def main():
    get_data_air_pollution()
    pre_preprocess_data_air_pollution()
    get_data_weather_history()
    pre_preprocess_data_weather_historical()
    merge_processed_data()


if __name__ == "__main__":
    main()
