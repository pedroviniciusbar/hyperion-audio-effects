FROM debian:stable
WORKDIR /app
RUN apt-get update && apt-get install -y libgstreamer1.0-0 libgstreamer1.0-0 gir1.2-gstreamer-1.0 gir1.2-glib-2.0 gir1.2-gst-plugins-base-1.0 gstreamer1.0-plugins-good gstreamer1.0-tools gstreamer1.0-alsa gstreamer1.0-pulseaudio python-gi python-tk python-pip
# COPY requirements.txt /app
COPY requirements.txt /app
RUN python -m  pip install -r requirements.txt
COPY . /app 
EXPOSE 8080
CMD ["python", "main.py", "--json", "--host=localhost", "--port=8080"]