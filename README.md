Hyperion audio effects
======================

##### Examples: https://www.youtube.com/watch?v=n-_0KG4EsY8 https://www.youtube.com/watch?v=HiAlv-mW9UI

Dev kit for creating audio visualizations for [hyperion](https://github.com/tvdzwan/hyperion).

- Update 8/4/2015: Some improvements and cleanup, new video
- Update 31/3/2015: New parameters and hyperion config file parsing

### Installation and running on Debian **

1. Install Gstreamer 1.0 and PyGI: `sudo apt-get install libgstreamer1.0-0 gir1.2-gstreamer-1.0 gir1.2-glib-2.0 gir1.2-gst-plugins-base-1.0 gstreamer1.0-plugins-good gstreamer1.0-tools gstreamer1.0-alsa gstreamer1.0-pulseaudio`
2. Install Tkinter for GUI: `sudo apt-get install python-tk`
3. Install pip: `sudo apt-get install python-pip`
4. Install dependencies: `sudo pip install -r requirements.txt` (or use virtualenv if you like)
5. Put `options snd-aloop index=-2` in end of `/etc/modprobe.d/alsa-base.conf` to prevent loopback device for getting first card index
6. Enable loopback device `modprobe snd-aloop`
7. Put the included `.asoundrc` to your home folder (backup old) and change the soundcard index if needed (`"hw:<card>,<device>"`, check `aplay -l`) *
8. Reboot or reload alsa `sudo alsa force-reload`
9. Run `python main.py` with options:
	- `--config=<path>` path to hyperion config file (defaults to `./hyperion.config.json`)
	- `--gui` for gui
	- `--json` for network connection (`--host=<ip> --port=<port>`)
	- `--help` to see all options
10. Play some audio
11. Levels should be drawn to gui, also sent to hyperion if json enabled
12. Exit by closing the GUI or Ctrl+c

### Effects development
1. Copy one of the script & config pairs in `effects/` (e.g. `myeffect.py` and `myeffect.json`) and then it can be passed as `--effect=myeffect` (json values can be read from `hyperion.args` like in normal hyperion effects)
2. Adjust gstreamer parameters
   - See `spectrum_dump.py` for explanation of parameters for GstSpectrumDump
   - Using `vumeter` and `bands` you can adjust the type of received magnitudes (`self.magnitudes`)
      * With `vumeter=True` you get 4 magnitudes which correspond to peaks and decays for the L/R channels
      * With `vumeter=False` you get spectrum magnitudes for the amount of `bands` (defaults to 128)
3. Update the leds by modifying the bytearray `self.ledsData` according to values in `self.magnitudes` (I've done it in method `update_leds()`)

### Effect: VU Meter
- Volume bars for left and right of your hyperion setup, or by setting indices manually
- Min and max volume and colors can be adjusted from config

### Effect: Color spectrum
- Leds strip is divided into octaves 1-8
- Low frequencies start from red, ending in pink at high frequencies
- Adjust your sound volume if the leds are too dim or bright (no volume normalization yet)
- Config has a field `band-width-exp`, if you have performance issues, try with higher values (it sets FFT bin size to 2^x Hz, e.g. 2^3 = 8 Hz, affects on bass accuracy)
- Set `mirror` to false if you want to use whole strip instead of splitting and mirroring
- TODO: Adjustable colors

\* Check this if you have pulseaudio: [#4](https://github.com/RanzQ/hyperion-audio-effects/issues/4#issuecomment-67764593)

\** Windows istructions were removed since performance was poor due to the fact that Gstreamer is meant for Linux
