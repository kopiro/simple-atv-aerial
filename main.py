#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime
import random
import requests
import shutil
import os

LIBRARY_URL = "http://a1.phobos.apple.com/us/r1000/000/Features/atv/AutumnResources/videos/entries.json"
CACHE_DIR = "./cache"
DAY_TIME = 4
NIGHT_TIME = 19


def download_file(url, file):
    print(f"Downloading {url} in {file}...")
    with requests.get(url, stream=True) as r:
        with open(file, 'wb') as f:
            shutil.copyfileobj(r.raw, f, 16*1024*1024)
    return file


def download_library():
    download_file(LIBRARY_URL, f"{CACHE_DIR}/library.json")


def load_videos():
    with open(f'{CACHE_DIR}/library.json') as json_file:
        data = json.load(json_file)
        videos = []
        for vid_group in data:
            for video in vid_group["assets"]:
                videos.append(video)
        random.shuffle(videos)
        return videos


def routine(videos):
    while True:
        for video in videos:
            now = datetime.now()
            now_time_of_day = ("day" if now.hour <
                               NIGHT_TIME and now.hour > DAY_TIME else "night")
            local_file = f"{CACHE_DIR}/{video['id']}.mov"
            time_of_day = video["timeOfDay"]
            if time_of_day == now_time_of_day:
                if not os.path.isfile(local_file):
                    download_file(video["url"], local_file)
                subprocess.call([os.getenv('MPLAYER'), local_file])


def main():
    download_library()
    routine(load_videos())


if __name__ == "__main__":
    main()
