import requests
from configs import INSULT_URL, GIPHY_URL, GIPHY_TOKEN

def get_insult_phrase():
    params = {"lang":"en", "type":"json"}
    response = requests.get(INSULT_URL, params=params)
    
    insult_json = response.json()
    insult_phrase = insult_json["insult"].replace('  ', ' ')

    return insult_phrase


def get_insult_gif():
    params = {"api_key": GIPHY_TOKEN}
    response = requests.get(GIPHY_URL, params=params)

    insult_json = response.json()
    insult_gif = insult_json.get("data").get("images").get("downsized").get("url")

    return insult_gif
