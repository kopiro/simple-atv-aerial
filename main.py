#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime
import random
import os

LIBRARY_URL = "http://a1.phobos.apple.com/us/r1000/000/Features/atv/AutumnResources/videos/entries.json"
CACHE_DIR = "./cache"
DAY_TIME = 4
NIGHT_TIME = 19


def download_file(url, file, defer=False):
    cmd = ["curl", "-s", url, "-o", file]
    if defer:
        print(f"Pre-downloading {url} in {file}...")
        subprocess.Popen(cmd)
    else:
        print(f"Downloading {url} in {file}...")
        subprocess.run(cmd)


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


def get_next_video_after(videos, fromIndex):
    index = fromIndex
    while True:
        index = (index + 1) % len(videos)
        video = videos[index]
        now = datetime.now()
        now_time_of_day = ("day" if now.hour <
                           NIGHT_TIME and now.hour > DAY_TIME else "night")
        time_of_day = video["timeOfDay"]
        if time_of_day == now_time_of_day:
            return video
        if index == fromIndex:
            return None


def get_local_file(video):
    return f"{CACHE_DIR}/{video['id']}.mov"


def routine(videos):
    index = len(videos) - 1
    while True:
        video = get_next_video_after(videos, index)
        local_file = get_local_file(video)
        if not os.path.isfile(local_file):
            download_file(video["url"], local_file)

        # Download next video defer
        next_video = get_next_video_after(videos, index)
        next_local_file = get_local_file(next_video)
        if not os.path.isfile(next_local_file):
            download_file(next_video["url"], get_local_file(next_video), True)

        # Show the video
        subprocess.call([os.getenv('MPLAYER'), "--fullscreen", local_file])


def main():
    download_library()
    routine(load_videos())


if __name__ == "__main__":
    main()
