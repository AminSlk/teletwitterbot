FROM python:3.8

RUN apt-get install -y wget
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt update
RUN apt install -y fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcups2 libdbus-1-3 libdrm2 libgbm1 libgtk-3-0 libnspr4 libnss3 libwayland-client0 libxcomposite1 libxdamage1 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils libu2f-udev libvulkan1
RUN apt-get install ./google-chrome-stable_current_amd64.deb
RUN mv /usr/bin/google-chrome /usr/bin/google-chrome-prev
COPY google-chrome /usr/bin/google-chrome
RUN chmod +x /usr/bin/google-chrome-prev
RUN chmod +x /usr/bin/google-chrome

RUN mkdir -p /home/mtest
WORKDIR /home/mtest
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV ENV_FOR_DYNACONF=production
COPY . .
CMD [ "python", "-m", "teletwitterbot" ]