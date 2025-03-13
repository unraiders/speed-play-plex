#!/bin/sh

echo "$(date +'%d-%m-%Y %H:%M:%S') - Arrancando entrypoint.sh" >&2
echo "$(date +'%d-%m-%Y %H:%M:%S') - Versión: $VERSION" >&2
echo "$(date +'%d-%m-%Y %H:%M:%S') - Zona horaria: $TZ" >&2
echo "$(date +'%d-%m-%Y %H:%M:%S') - Cliente torrent: $CLIENTE_TORRENT" >&2
echo "$(date +'%d-%m-%Y %H:%M:%S') - Debug: $DEBUG" >&2
echo "$(date +'%d-%m-%Y %H:%M:%S') - Arrancando servidor..." >&2

exec gunicorn --bind 0.0.0.0:9898 --workers 1 speed-play-plex:app