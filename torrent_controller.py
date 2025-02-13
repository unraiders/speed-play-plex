import requests
from transmission_rpc import Client
from utils import setup_logger
from config import *

# Inicializar el logger
logger = setup_logger(__name__)

class TorrentController:
    def __init__(self):
        self.client_type = CLIENTE_TORRENT.lower()
        self.host = CLIENTE_TORRENT_IP
        self.port = CLIENTE_TORRENT_PORT
        self.username = CLIENTE_TORRENT_USER
        self.password = CLIENTE_TORRENT_PASSWORD
        self.session = None

    def connect(self):
        if self.client_type == 'qbittorrent':
            return self._connect_qbittorrent()
        elif self.client_type == 'transmission':
            return self._connect_transmission()
        else:
            logger.error(f"Cliente torrent no soportado: {self.client_type}")
            return False

    def _connect_qbittorrent(self):
        try:
            self.session = requests.Session()
            login_url = f"http://{self.host}:{self.port}/api/v2/auth/login"
            logger.debug(f"Intentando conectar a qBittorrent en {login_url}")
            response = self.session.post(
                login_url,
                data={'username': self.username, 'password': self.password}
            )
            if response.status_code == 200 and response.text == "Ok.":
                logger.info("Conectado a qBittorrent exitosamente")
                return True
            else:
                logger.error(f"Error al conectar con qBittorrent. Código: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error de conexión con qBittorrent: {str(e)}")
            return False

    def _check_qbittorrent_connection(self):
        try:
            response = self.session.get(f"http://{self.host}:{self.port}/api/v2/app/version")
            if response.status_code == 200:
                return True
            logger.debug("Sesión expirada, intentando reconectar...")
            return self._connect_qbittorrent()
        except:
            return self._connect_qbittorrent()

    def _connect_transmission(self):
        try:
            logger.debug(f"Intentando conectar a Transmission en {self.host}:{self.port}")
            self.session = Client(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password
            )
            logger.info("Conectado a Transmission exitosamente")
            return True
        except Exception as e:
            logger.error(f"Error de conexión con Transmission: {str(e)}")
            return False

    def toggle_speed_limit(self, enable=True):
        logger.debug(f"Intentando {'activar' if enable else 'desactivar'} límite de velocidad")
        if self.client_type == 'qbittorrent':
            return self._toggle_qbittorrent_speed_limit(enable)
        elif self.client_type == 'transmission':
            return self._toggle_transmission_speed_limit(enable)

    def _toggle_qbittorrent_speed_limit(self, enable):
        try:
            if not self._check_qbittorrent_connection():
                raise Exception("No se pudo establecer conexión con qBittorrent")

            response = self.session.get(f"http://{self.host}:{self.port}/api/v2/transfer/speedLimitsMode")
            if response.status_code != 200:
                raise Exception(f"Error al obtener el modo actual. Código: {response.status_code}")
            
            current_mode = int(response.text)
            logger.debug(f"Estado actual del límite de velocidad: {current_mode}")
            
            if (enable and not current_mode) or (not enable and current_mode):
                toggle_url = f"http://{self.host}:{self.port}/api/v2/transfer/toggleSpeedLimitsMode"
                logger.debug(f"Cambiando límite de velocidad usando {toggle_url}")
                response = self.session.post(toggle_url)
                if response.status_code != 200:
                    raise Exception(f"Error al cambiar el límite de velocidad. Código: {response.status_code}")
                logger.info(f"Límite de velocidad {'activado' if enable else 'desactivado'}")
            return True
        except Exception as e:
            logger.error(f"Error al cambiar límite de velocidad en qBittorrent: {str(e)}")
            return False

    def _toggle_transmission_speed_limit(self, enable):
        try:
            logger.info(f"Cambiando límite de velocidad en Transmission a: {'activado' if enable else 'desactivado'}")
            self.session.set_session(
                alt_speed_enabled=enable,
            )
            logger.debug("Nueva configuración de la sesión aplicada")
            return True
        except Exception as e:
            logger.error(f"Error al cambiar límite de velocidad en Transmission: {str(e)}")
            return False
