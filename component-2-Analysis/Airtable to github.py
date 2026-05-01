import json
import requests

api_key = ("pat4TEKjHaDy6fXyi.3a2449a91eb923c1c6509eac28b0e78e59479f498af8ee583b940cef16cc1858")
url = "https://api.airtable.com/v0/appdNv0F6L4BbHMDb/Alerts"


headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}



r = requests.get(url, headers=headers)

with open("ALERT.json", "w") as f:
    json.dump(r.json(), f, indent=4)
