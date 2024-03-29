import json
import os
from datetime import date

import pandas as pd

file_location = os.path.dirname(__file__)


def pre_preprocess_data_air_pollution():
    print("--- Started air pollution data pre-processing ---")

    csv_filename = os.path.join(file_location, "../../data/processed/processed_data_air_pollution.csv")
    raw_data_filename = os.path.join(file_location,
                                     "../../data/raw/air/raw_data_" + date.today().strftime("%b-%d-%Y") + ".json")
    raw_file = open(raw_data_filename, "r+")

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


if __name__ == "__main__":
    pre_preprocess_data_air_pollution()