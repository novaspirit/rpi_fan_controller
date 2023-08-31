# --- Reference: https://iotbytes.wordpress.com/create-your-first-docker-container-for-raspberry-pi-to-blink-an-led/

# - Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM python:3.9


# - Install necessary dependencies (required for temperature measurement (vcgencmd))
# https://stackoverflow.com/a/49462622
#ARG APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1

RUN apt update \
 && apt install wget \
 && wget -O - https://archive.raspbian.org/raspbian.public.key | apt-key add - \
 && wget -O - http://archive.raspberrypi.org/debian/raspberrypi.gpg.key | apt-key add - \
 && echo 'deb http://archive.raspberrypi.org/debian/ bullseye main' | tee -a /etc/apt/sources.list \
 && apt update  \
 && apt install -y --no-install-recommends \
                libraspberrypi-bin \
 && apt autoremove \
 && rm -rf /tmp/* \
 && rm -rf /var/lib/apt/lists/*


# - Intall the rpi.gpio python module
RUN pip install --no-cache-dir rpi.gpio


# - Create user (for security)
# RUN useradd --create-home pwmuser
# USER pwmuser


# - Copy Python script
WORKDIR /usr/local/bin
COPY src/fan_control.py .


# - Run python script ('-u' -> unbuffered output => output both stderr & stdout during runtime)
CMD ["python", "-u", "fan_control.py"]
