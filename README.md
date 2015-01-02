Hyperion audio effects
======================

##### Examples: https://www.youtube.com/watch?v=Hv3B8iVsPho https://www.youtube.com/watch?v=LNv7K-viZZw

Dev kit for creating audio visualizations for [hyperion](https://github.com/tvdzwan/hyperion).

- Based on https://github.com/Fabi1080/hyperion_effects_dev_kit
- Also uses this neat wrapper (modified for Gstreamer 1.0) https://github.com/Wintervenom/gst-spectrumdump
- Pull requests or improvement suggestions welcome
- Not sure if it's possible get the hyperion effects engine to import PyGI, so for now these effects must be run separately using the json connection

### Installation and running on Debian

1. Install Gstreamer 1.0 and PyGI: `libgstreamer1.0-0 gir1.2-gstreamer-1.0 gir1.2-glib-2.0 gir1.2-gst-plugins-base-1.0 gstreamer1.0-plugins-good gstreamer1.0-tools gstreamer1.0-alsa gstreamer1.0-pulseaudio`
2. Install Tkinter for GUI: `apt-get install python-tk`
3. Set hyperion settings in main.py
4. Put `options snd-aloop index=-2` in end of `/etc/modprobe.d/alsa-base.conf` to prevent loopback device for getting first card index
5. Enable loopback device `modprobe snd-aloop`
6. Put the included `.asoundrc` to your home folder (backup old) and change the soundcard index if needed (`"hw:<card>,<device>"`, check `aplay -l`) *
7. Reboot or reload alsa `sudo alsa force-reload`
8. Run `python main.py` (`--gui` for gui, `--json` for network connection)
9. Play some audio
10. Levels should be drawn to gui, also sent to hyperion if json enabled
11. Exit by closing the GUI or Ctrl+c

### Installation and running on Windows **

1. Install Python 2.7 (set python to PATH)
2. Install needed components from PyGI AIO: http://sourceforge.net/projects/pygobjectwin32/files/
   - Do you have portable? No
   - Choose destination: 2.7
   - Choose packages: Base packages, Gst-plugins, Gst-plugins-extra, Gstreamer
   - Do you want classic? No
   - Install
3. Select "Stereo mix" as recording device (if available, or mic)
3. Set hyperion settings in main.py
4. Run `python main.py` (`--gui` for gui, `--json` for network connection)
5. Play some audio
6. Levels should be drawn to gui, also sent to hyperion if json enabled
7. Exit by closing the GUI or Ctrl+c

### Effects development
1. Copy one of the script & config pairs in `effects/` (e.g. `myeffect.py` and `myeffect.json`) and then it can be passed as `--effect=myeffect` (json values can be read from `hyperion.args` like in normal hyperion effects)
2. Adjust gstreamer parameters
   - See `spectrum_dump.py` for explanation of parameters for GstSpectrumDump
   - Using `vumeter` and `bands` you can adjust the type of received magnitudes (`self.magnitudes`)
      * With `vumeter=True` you get 4 magnitudes which correspond to peaks and decays for the L/R channels
      * With `vumeter=False` you get spectrum magnitudes for the amount of `bands` (defaults to 128)
3. Update the leds by modifying the bytearray `self.ledsData` according to values in `self.magnitudes` (I've done it in method `update_leds()`)

\* Check this if you have pulseaudio: [#4](https://github.com/RanzQ/hyperion-audio-effects/issues/4#issuecomment-67764593)

\** Trying to figure out what is the bottleneck on Windows, doesn't run very smoothly
