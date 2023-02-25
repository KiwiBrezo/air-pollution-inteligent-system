import json
import urllib.request
import pandas as pd


def get_data():
    url = "https://arsoxmlwrapper.app.grega.xyz/api/air/archive"

    print("--- Started download ---")
    with urllib.request.urlopen(url) as response:
        raw_file = open("../../data/raw/raw_data.json", "w")

        print("--- Done download, saving to file ---")

        raw_file.write(response.read().decode('utf-8'))
        raw_file.close()

        print("--- Done saving to file ---")


def process_data():
    print("--- Started data processing ---")

    raw_file = open("../../data/raw/raw_data.json", "r")

    data = json.load(raw_file)
    meteoroloske_data = []

    for item in data:
        item_json = json.loads(item["json"])
        item_arr_postaj = item_json["arsopodatki"]["postaja"]
        item_postaja_data = [x for x in item_arr_postaj if x["merilno_mesto"] == "Ptuj"]

        meteoroloske_data.append(item_postaja_data[0])

    lst = [[x["datum_do"], x["ge_dolzina"], x["ge_sirina"], x["merilno_mesto"], x["nadm_visina"], x["pm2.5"], x["pm10"], x["sifra"]] for x in meteoroloske_data]
    df = pd.DataFrame(lst, columns=["datum_do", "ge_dolzina", "ge_sirina", "merilno_mesto", "nadm_visina", "pm25", "pm10", "sifra"])
    df.to_csv('../../data/processed/processed_data.csv', index=False, header=True)

    print("--- Done data processing ---")


if __name__ == "__main__":
    get_data()
    process_data()
