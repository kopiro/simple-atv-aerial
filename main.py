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
    cmd = ["curl", url, "-o", file]
    if defer:
        print(f"Pre-downloading {url} in {file}...")
        return subprocess.Popen(cmd)
    else:
        print(f"Downloading {url} in {file}...")
        return subprocess.run(cmd)


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


def is_video_criteriamet(video):
    now = datetime.now()
    now_time_of_day = ("day" if now.hour <
                       NIGHT_TIME and now.hour > DAY_TIME else "night")
    time_of_day = video["timeOfDay"]
    return time_of_day == now_time_of_day


def get_local_file(video):
    return f"{CACHE_DIR}/{video['id']}.mov"


def is_video_downloaded(video):
    return os.path.isfile(get_local_file(video))


def get_next_video(videos, fromIndex):
    index = fromIndex
    while True:
        index = (index + 1) % len(videos)
        video = videos[index]
        if is_video_criteriamet(video):
            return index, video
        if index == fromIndex:
            return None


def get_first_video(videos):
    for index, video in enumerate(videos):
        if is_video_criteriamet(video):
            return index, video


def get_downloaded_videos(videos):
    downloaded_videos = []
    for index, video in enumerate(videos):
        if is_video_criteriamet(video) and is_video_downloaded(video):
            downloaded_videos.append([index, video])
    return downloaded_videos


def play_video(video):
    file = get_local_file(video)
    player = os.getenv('MPLAYER')
    if player == "omxplayer":
        subprocess.call([player, file])
    elif player == "vlc":
        subprocess.call([player, "--fullscreen", "--play-and-exit", file])
    else:
        subprocess.call([player, file])


def download_video(video, defer=False):
    local_file = get_local_file(video)
    if not os.path.isfile(local_file):
        return download_file(video["url"], local_file, defer)


def routine(videos):
    video = None
    index = None
    while True:
        if video == None:
            downloaded_videos = get_downloaded_videos(videos)
            if len(downloaded_videos) > 0:
                index, video = random.choice(downloaded_videos)
            else:
                index, video = get_first_video(videos)
                download_video(video)

        # Download next video in async
        next_index, next_video = get_next_video(videos, index)
        if not is_video_downloaded(next_video):
            download_video(next_video, True)

        # Show the video
        play_video(video)
        video = None

        if is_video_downloaded(next_video):
            video = next_video
            index = next_index


def main():
    if not os.getenv('MPLAYER'):
        print("Please configure your MPLAYER environment variable")
        exit()

    download_library()
    routine(load_videos())


if __name__ == "__main__":
    main()
