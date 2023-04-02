import os

import pandas as pd

file_location = os.path.dirname(__file__)


def merge_processed_data():
    print("--- Started margin data ---")

    air_pollution_csv_filename = os.path.join(file_location, "../../data/processed/processed_data_air_pollution.csv")
    historical_weather_csv_filename = os.path.join(file_location, "../../data/processed"
                                                                  "/processed_data_historical_weather.csv")
    merged_csv_filename = os.path.join(file_location, "../../data/processed/current_processed_data_merged.csv")

    df_air_pollution = pd.read_csv(air_pollution_csv_filename)
    df_historical_weather = pd.read_csv(historical_weather_csv_filename)

    df_air_pollution = df_air_pollution.sort_values("datum_do")
    df_historical_weather = df_historical_weather.sort_values("datum_do")

    df_merged = df_historical_weather.merge(df_air_pollution, how="outer").sort_values("datum_do")

    number_of_rows_before = len(df_merged.index)

    #Odstranimo vse vrstice v katerih se pojavi podatek NaN
    #df_merged = df_merged.dropna()

    number_of_rows_after = len(df_merged.index)

    print("     -> Marged dataframe was reduced by", number_of_rows_before - number_of_rows_after, "rows")

    df_merged.to_csv(merged_csv_filename, index=False, header=True)

    print("     -> Done margin data")


if __name__ == "__main__":
    merge_processed_data()