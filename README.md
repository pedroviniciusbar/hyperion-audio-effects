Hyperion Gstreamer audio effects
================================

Dev kit for creating audio visualizations for [hyperion](https://github.com/tvdzwan/hyperion). W.I.P. Requires `Tkinter` (for dev gui) and `pygst`.

- Based on https://github.com/Fabi1080/hyperion_effects_dev_kit
- Also uses this neat wrapper (slightly modified) https://github.com/Wintervenom/gst-spectrumdump
- Gstreamer pipeline seems to freeze often (I just keep killing the python process when that happens, issue with threads maybe?)
- Tested with leds using the json-connection: https://www.youtube.com/watch?v=sC_dO7YTh4o
- Pull requests or improvement suggestions welcome, would be nice to get this working with PyGI or plain python (alsaaudio)
- Not sure yet how to get the effects engine to run pygst

### Installation in Debian

1. Install `python-gst0.10` and `python-tk`
2. Set hyperion settings in main.py, comment `json_client.open_connection()` if needed
3. Run `python main.py`
4. Play some audio
