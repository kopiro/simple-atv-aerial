# simple-atv-aerial

Simple Apple TV Aerial screensaver, works on any OSX that can run Python and has a movie player.

### installation

You need to install `python3`, `pip3` and `pipenv`.

Also, you need a video player that is launchable from CLI and set its binary as environment variable called `MPLAYER`.

For Raspberry PI, I recommend `omxplayer`.

```sh
git clone https://github.com/kopiro/simple-atv-aerial.git
cd simple-atv-aerial
pipenv install
```

### launch

```sh
./main.py
```
