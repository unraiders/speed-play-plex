import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

DEBUG = os.getenv("DEBUG_MODE", "0") == "1"

TAUTULLI_API_KEY = os.getenv('TAUTULLI_API_KEY')
TAUTULLI_IP = os.getenv('TAUTULLI_IP')
TAUTULLI_PORT = os.getenv('TAUTULLI_PORT')

CLIENTE_TORRENT_IP = os.getenv('CLIENTE_TORRENT_IP')
CLIENTE_TORRENT_PORT = os.getenv('CLIENTE_TORRENT_PORT')
CLIENTE_TORRENT_USER = os.getenv('CLIENTE_TORRENT_USER')
CLIENTE_TORRENT_PASSWORD = os.getenv('CLIENTE_TORRENT_PASSWORD')

# Opciones: qbittorrent o transmission
CLIENTE_TORRENT = os.getenv('CLIENTE_TORRENT', '').lower()



