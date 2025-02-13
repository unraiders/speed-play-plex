FROM python:3.11-alpine

LABEL maintainer="unraiders"
LABEL version="1.0.0"
LABEL description="Control de velocidad clientes torrent basado en la actividad de Plex (API Tautulli)."

RUN adduser -D speedplay

WORKDIR /app

COPY requirements.txt .
COPY utils.py .
COPY config.py .
COPY torrent_controller.py .
COPY speed-play-plex.py .

RUN pip install --no-cache-dir -r requirements.txt && \
    chown -R speedplay:speedplay /app

EXPOSE 9898

USER speedplay

CMD ["gunicorn", "--bind", "0.0.0.0:9898", "--workers", "2", "speed-play-plex:app"]