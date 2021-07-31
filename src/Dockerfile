FROM debian:stable
WORKDIR /app
RUN apt-get update && apt-get install -y wget gnupg  gnupg2 gnupg1 sudo
RUN wget https://github.com/hyperion-project/hyperion.ng/releases/download/2.0.0-alpha.10/Hyperion-2.0.0-alpha.10-Linux-x86_64.deb
RUN apt-get install ./Hyperion-2.0.0-alpha.10-Linux-x86_64.deb -y
RUN apt-get install -y libgstreamer1.0-0 libgstreamer1.0-0 gir1.2-gstreamer-1.0 gir1.2-glib-2.0 gir1.2-gst-plugins-base-1.0 gstreamer1.0-plugins-good gstreamer1.0-tools gstreamer1.0-alsa gstreamer1.0-pulseaudio python-gi python-tk python-pip
COPY requirements.txt /app
RUN python -m  pip install -r requirements.txt
COPY . /app 
EXPOSE 8080
# CMD ["bash"]
CMD ["python", "main.py", "--config=/app/hyperion.config.json", "--json", "--port=8080", "--gui"]