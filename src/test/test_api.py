import requests


def test_fetch_api():
    response = requests.get("https://arsoxmlwrapper.app.grega.xyz/api/")
    assert response.status_code == 200
    response = requests.get("https://open-meteo.com/")
    assert response.status_code == 200
