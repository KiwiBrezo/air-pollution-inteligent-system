import os
import urllib
from datetime import date

file_location = os.path.dirname(__file__)


def get_data_air_pollution():
    url = "https://arsoxmlwrapper.app.grega.xyz/api/air/archive"

    print("--- Started download air pollution raw data ---")
    print("     -> Getting data from: ", url)
    with urllib.request.urlopen(url) as response:
        raw_data_filename = os.path.join(file_location,
                                         "../../data/raw/air/raw_data_" + date.today().strftime("%b-%d-%Y") + ".json")
        raw_file = open(raw_data_filename, "wb+")

        print("     -> Done download, saving to file...")

        raw_file.write(response.read())
        raw_file.close()

        print("     -> Done saving to file")


if __name__ == "__main__":
    get_data_air_pollution()
