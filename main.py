#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime
import random
import os
import sys
from pathlib import Path
import errno

HOME = str(Path.home())
LIBRARY_URL = "http://a1.phobos.apple.com/us/r1000/000/Features/atv/AutumnResources/videos/entries.json"
CACHE_DIR = os.path.join(HOME, ".simple-atv-aerial")
DAY_TIME = 4
NIGHT_TIME = 19


def load_videos():
    now = datetime.now()
    now_time_of_day = ("day" if now.hour <
                       NIGHT_TIME and now.hour > DAY_TIME else "night")
    now_path = os.path.join(CACHE_DIR, now_time_of_day)
    return [os.path.join(now_path, f) for f in os.listdir(now_path)]


def get_local_file(video):
    return os.path.join(CACHE_DIR, video['timeOfDay'], f"{video['id']}.mov")


def play_video(file):
    player = os.getenv('MPLAYER')
    if player == "omxplayer":
        subprocess.call([player, file])
    elif player == "vlc":
        subprocess.call([player, "--fullscreen", "--play-and-exit", file])
    else:
        subprocess.call([player, file])


def download_file(url, file):
    cmd = ["curl", url, "-o", file]
    return subprocess.run(cmd)


def download_video(video):
    local_file = get_local_file(video)
    try:
        os.makedirs(os.path.dirname(local_file), 0o755)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    if not os.path.isfile(local_file):
        return download_file(video["url"], local_file)


def download_library():
    try:
        os.makedirs(CACHE_DIR, 0o755)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    lib_file = os.path.join(CACHE_DIR, "library.json")
    download_file(LIBRARY_URL, lib_file)

    with open(lib_file) as json_file:
        data = json.load(json_file)
        for vid_group in data:
            for video in vid_group["assets"]:
                download_video(video)


def routine():
    while True:
        files = load_videos()
        file = random.choice(files)
        play_video(file)


def main():
    if not os.getenv('MPLAYER'):
        print("Please configure your MPLAYER environment variable")
        exit()

    if len(sys.argv) >= 2 and sys.argv[1] == '--download':
        download_library()
        return

    routine()


if __name__ == "__main__":
    main()
