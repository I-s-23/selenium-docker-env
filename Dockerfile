FROM python:3.9.6-slim-buster
COPY . .
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    wget \
    gnupg \
    poppler-utils \
    scrot \
    pkg-config \
    libcairo2-dev \
    xxd \
    fonts-ipafont \
    python3-tk python3-dev \
    # Install Chrome
    dbus-x11 libssl1.1 \
    && wget https://dl.google.com/linux/linux_signing_key.pub \
    && apt-key add linux_signing_key.pub \
    && echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get -y update \
    && apt update \
    && apt-get -y install google-chrome-stable \
    && apt install -y xvfb xserver-xephyr software-properties-common libgirepository1.0-dev libssl-dev \
    xvfb xserver-xephyr \
    && python -m pip install -U pip setuptools \
    && pip install -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN Xvfb :99 -ac &
