import requests
from datetime import datetime, timedelta

BASE_URL = "https://uczen.eduvulcan.pl/powiatzdunskowolski/api/PlanZajec"

def fetch_week(cookies: dict, key: str, date_from: datetime) -> dict:
    date_to = date_from + timedelta(days=6, hours=23, minutes=59, seconds=59, milliseconds=999)
    params = {
        "key": key,
        "dataOd": date_from.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "dataDo": date_to.strftime("%Y-%m-%dT%H:%M:%S.999Z"),
        "zakresDanych": 2
    }
    response = requests.get(BASE_URL, params=params, cookies=cookies)
    return response.json()