import csv
import json
import os
import sys

import dotenv
import requests
from bs4 import BeautifulSoup

if len(sys.argv < 2):
    print("Usage: python apple_export.py <filename>")
    exit()

dotenv.load_dotenv()
r = requests.get(os.environ["APPLE_URL"])

if r.status_code != 200:
    raise requests.HTTPError(response=r)

server_data = json.loads(
    BeautifulSoup(r.text, "html.parser").find(id="serialized-server-data").text
)

with open(sys.argv[1], "w") as file:
    writer = csv.writer(file, delimiter=";")

    writer.writerows(
        map(
            lambda item: (item["title"], item["artistName"]),
            server_data[0]["data"]["sections"][1]["items"],
        )
    )
