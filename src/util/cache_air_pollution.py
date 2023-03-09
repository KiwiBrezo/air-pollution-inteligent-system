import json
import time

import requests

meteoroloske_data_cache = None
is_cached = False


def cache_meteoroloske_data():
    global is_cached, meteoroloske_data_cache

    print("--- Started refreshing cache ---")

    response = requests.get("https://arsoxmlwrapper.app.grega.xyz/api/air/archive")
    ptuj_data = json.loads(response.text)

    is_cached = False
    meteoroloske_data_cache = []

    for item in ptuj_data:
        item_json = json.loads(item["json"])
        item_arr_postaj = item_json["arsopodatki"]["postaja"]
        item_postaja_data = [x for x in item_arr_postaj if x["merilno_mesto"] == "Ptuj"]

        meteoroloske_data_cache.append(item_postaja_data[0])

    is_cached = True

    print("     -> Done refreshing cache")

    #set_cache_timeout()


def set_cache_timeout():
    time.sleep(60 * 30)
    cache_meteoroloske_data()


def init_cache():
    cache_meteoroloske_data()


def get_meteoroloske_data():
    global is_cached, meteoroloske_data_cache

    if not is_cached:
        time.sleep(2)
        return get_meteoroloske_data()

    return meteoroloske_data_cache
