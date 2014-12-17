Hyperion audio effects
======================

* New test video: https://www.youtube.com/watch?v=2Htkz8nhu-E

Dev kit for creating audio visualizations for [hyperion](https://github.com/tvdzwan/hyperion).

- Based on https://github.com/Fabi1080/hyperion_effects_dev_kit
- Also uses this neat wrapper (modified for Gstreamer 1.0) https://github.com/Wintervenom/gst-spectrumdump
- Tested with leds using the json-connection: https://www.youtube.com/watch?v=sC_dO7YTh4o
- Pull requests or improvement suggestions welcome
- Not sure yet how to get the hyperion effects engine to import PyGI
- Tested without pulseaudio (alsa only)

### Installation on Debian

1. Install Gstreamer 1.0 and PyGI: `apt-get install python-gi gir1.2-glib-2.0 gir1.2-gnomebluetooth-1.0 gir1.2-gst-plugins-base-1.0 gir1.2-gstreamer-1.0 gstreamer1.0-alsa gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-pulseaudio gstreamer1.0-tools gstreamer1.0-x libgstreamer-plugins-base1.0-0 libgstreamer1.0-0` (this is what I have now installed, not sure if all of them are required)
2. Install Tkinter for GUI: `apt-get install python-tk`
3. Set hyperion settings in main.py
4. Put `options snd-aloop index=-2` in end of `/etc/modprobe.d/alsa-base.conf` to prevent loopback device for getting first card index
5. Enable loopback device `modprobe snd-aloop`
6. Put the included `.asoundrc` to your home folder (backup old) and change the soundcard index if needed (`"hw:<card>,<device>"`, check `aplay -l`)
7. Run `python main.py` (`--gui` for gui, `--json` for network connection)
8. Play some audio
9. Levels should be drawn to gui, also sent to hyperion if json enabled
