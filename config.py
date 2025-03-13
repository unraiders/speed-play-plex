import os

from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Opciones: qbittorrent, transmission o synology_ds
CLIENTE_TORRENT = os.getenv('CLIENTE_TORRENT', '').lower()

TAUTULLI_IP = os.getenv('TAUTULLI_IP')
TAUTULLI_PORT = os.getenv('TAUTULLI_PORT')
TAUTULLI_API_KEY = os.getenv('TAUTULLI_API_KEY')

CLIENTE_TORRENT_IP = os.getenv('CLIENTE_TORRENT_IP')
CLIENTE_TORRENT_PORT = os.getenv('CLIENTE_TORRENT_PORT')
CLIENTE_TORRENT_USER = os.getenv('CLIENTE_TORRENT_USER')
CLIENTE_TORRENT_PASSWORD = os.getenv('CLIENTE_TORRENT_PASSWORD')

TZ = os.getenv("TZ", "Europe/Madrid")
DEBUG = os.getenv("DEBUG", "0") == "1"



