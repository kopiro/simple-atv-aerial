# simple-atv-aerial

Simple Apple TV Aerial screensaver, works on any OSX that can run Python and has a movie player.

### installation

You need to install `python3` and `curl`.

Also, you need a video player that is launchable from CLI and set its binary as environment variable called `MPLAYER`.

For Raspberry PI, I recommend the default `omxplayer`.

```sh
git clone https://github.com/kopiro/simple-atv-aerial.git
cd simple-atv-aerial
```

### first download

You want to download the videos before running it for the first time.

You can stop the script anytime if you want to test it before:

```sh
./main.py --download
```

### launch

```sh
./main.py
```
