FROM python:3.12-alpine

LABEL maintainer="unraiders"
LABEL description="Control de velocidad clientes torrents qBittorrent, Transmission, Synology Download Station y rTorrent basado en la actividad de Plex (API Tautulli)."

ARG VERSION=1.3.0
ENV VERSION=${VERSION}

RUN adduser -D speedplay

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN chown -R speedplay:speedplay /app

COPY utils.py .
COPY config.py .
COPY torrent_controller.py .
COPY speed-play-plex.py .

EXPOSE 9898

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

USER speedplay

ENTRYPOINT ["/app/entrypoint.sh"]