Hyperion Gstreamer audio effects
================================

Dev kit for creating audio visualizations for [hyperion](https://github.com/tvdzwan/hyperion). Requires `Tkinter` (for dev gui) and `pygst`.

- Based on https://github.com/Fabi1080/hyperion_effects_dev_kit
- Also uses this neat wrapper (slightly modified) https://github.com/Wintervenom/gst-spectrumdump
- Gstreamer pipeline seems to freeze often (I just keep killing the python process when that happens, issue with threads maybe?)
- Tested with leds using the json-connection: https://www.youtube.com/watch?v=sC_dO7YTh4o
- Pull requests or improvement suggestions welcome
- Not sure yet how to get the hyperion effects engine to run pygst
- Tested without pulseaudio (alsa only)
- Currently trying to figure out what causes delay

### Installation in Debian

1. Install `python-gst0.10` and `python-tk` (if you want gui)
2. Set hyperion settings in main.py
2. Put `options snd-aloop index=-2` in end of `/etc/modprobe.d/alsa-base.conf` to prevent loopback device for getting first card index
2. Enable loopback device `modprobe snd-aloop`
3. Put the included `.asoundrc` to your home folder (backup old) and change the soundcard index if needed (`"hw:<card>,<device>"`, check `aplay -l`)
3. Run `python main.py` (`--gui` for gui, `--json` for network connection)
4. Play some audio
5. Levels should be printed to stdout and drawn to gui, also sent to hyperion if json enabled