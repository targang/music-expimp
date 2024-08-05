import csv
import os
import sys
from tqdm import tqdm

import dotenv
from yandex_music import Client


dotenv.load_dotenv()


def load_csv() -> list[tuple[str, str]]:
    if len(sys.argv) < 2:
        print("Usage: python yandex_import.py <filename>")
        exit()
    with open(sys.argv[1], "r") as file:
        reader = csv.reader(file, delimiter=";")
        return [(title, artist) for title, artist in reader]


data = load_csv()


TOKEN = os.environ["YANDEX_TOKEN"]

client: Client = Client(TOKEN).init()

counter = 0
revision = int(os.environ["YANDEX_REVISION"])
for data_track in tqdm(data):
    search = client.search(" ".join(data_track), type_="track")
    # трек не найден
    if not search or not search.tracks or search.tracks.total == 0:
        continue
    counter += 1
    track = search.tracks.results[0]
    if len(track.albums) == 0:
        continue
    client.users_playlists_insert_track(
        os.environ["YANDEX_TARGET"], track.id, track.albums[0].id, revision=revision
    )
    revision += 1
