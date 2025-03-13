import time

from qbittorrentapi import Client as qbClient
from synology_api.downloadstation import DownloadStation as synoClient
from transmission_rpc import Client as transClient

from config import (
    CLIENTE_TORRENT,
    CLIENTE_TORRENT_IP,
    CLIENTE_TORRENT_PASSWORD,
    CLIENTE_TORRENT_PORT,
    CLIENTE_TORRENT_USER,
)
from utils import setup_logger

logger = setup_logger(__name__)

class TorrentController:
    def __init__(self):
        self.client_type = CLIENTE_TORRENT.lower()
        self.host = CLIENTE_TORRENT_IP
        self.port = CLIENTE_TORRENT_PORT
        self.username = CLIENTE_TORRENT_USER
        self.password = CLIENTE_TORRENT_PASSWORD
        self.client = None

    def connect(self, max_retries=float("inf"), retry_delay=5):
        if self.client_type == 'qbittorrent':
            self.client = self._connect_qbittorrent(max_retries, retry_delay)
        elif self.client_type == 'transmission':
            self.client = self._connect_transmission(max_retries, retry_delay)
        elif self.client_type == 'synology_ds':
            self.client = self._connect_synology_ds(max_retries, retry_delay)
        else:
            logger.error(f"Cliente torrent no soportado: {self.client_type}")
            return False
        return self.client is not None

    def _connect_qbittorrent(self, max_retries=float("inf"), retry_delay=5):
        attempts = 0
        while attempts < max_retries:
            try:
                client = qbClient(
                    host=f"http://{CLIENTE_TORRENT_IP}:{CLIENTE_TORRENT_PORT}",
                    username=CLIENTE_TORRENT_USER,
                    password=CLIENTE_TORRENT_PASSWORD,
                )
                client.auth_log_in()
                logger.info("Conectado a qBittorrent")
                return client
            except Exception as e:
                attempts += 1
                logger.error(f"Fallo al conectar a qBittorrent (intento {attempts}): {str(e)}")
                if attempts < max_retries:
                    logger.info(f"Reintentando en {retry_delay} segundos...")
                    time.sleep(retry_delay)
                else:
                    raise Exception("Max reintentos. No se puede establecer conexión con qBittorrent")

    def _connect_transmission(self, max_retries=float("inf"), retry_delay=5):
        attempts = 0
        while attempts < max_retries:
            try:
                client = transClient(
                    host=CLIENTE_TORRENT_IP,
                    port=CLIENTE_TORRENT_PORT,
                    username=CLIENTE_TORRENT_USER,
                    password=CLIENTE_TORRENT_PASSWORD,
                )
                logger.info("Conectado a Transmission")
                return client
            except Exception as e:
                attempts += 1
                logger.error(f"Fallo al conectar a Transmission (intento {attempts}): {str(e)}")
                if attempts < max_retries:
                    logger.info(f"Reintentando en {retry_delay} segundos...")
                    time.sleep(retry_delay)
                else:
                    raise Exception("Max reintentos. No se puede establecer conexión con Transmission")

    def _connect_synology_ds(self, max_retries=float("inf"), retry_delay=5):
        attempts = 0
        while attempts < max_retries:
            try:
                client = synoClient(
                    CLIENTE_TORRENT_IP,
                    CLIENTE_TORRENT_PORT,
                    CLIENTE_TORRENT_USER,
                    CLIENTE_TORRENT_PASSWORD,
                )
                logger.info("Conectado a Synology Download Station")
                return client
            except Exception as e:
                attempts += 1
                logger.error(f"Fallo al conectar a Synology Download Station (intento {attempts}): {str(e)}")
                if attempts < max_retries:
                    logger.info(f"Reintentando en {retry_delay} segundos...")
                    time.sleep(retry_delay)
                else:
                    raise Exception("Max reintentos. No se puede establecer conexión con Synology Download Station")

    def toggle_speed_limit(self, enable=True):
        logger.debug(f"Intentando {'activar' if enable else 'desactivar'} límite de velocidad")
        if self.client_type == 'qbittorrent':
            return self._toggle_qbittorrent_speed_limit(enable)
        elif self.client_type == 'transmission':
            return self._toggle_transmission_speed_limit(enable)
        elif self.client_type == 'synology_ds':
            return self._toggle_synology_ds_speed_limit(enable)

    def _toggle_qbittorrent_speed_limit(self, enable):
        try:
            logger.info(f"Cambiando límite de velocidad en qBittorrent a: {'activado' if enable else 'desactivado'}")
            self.client.transfer.toggle_speed_limits_mode(enable)
            logger.debug("Nueva configuración de la sesión aplicada")
            return True
        except Exception as e:
            logger.error(f"Error al cambiar límite de velocidad en qBittorrent: {str(e)}")
            return False

    def _toggle_transmission_speed_limit(self, enable):
        try:
            logger.info(f"Cambiando límite de velocidad en Transmission a: {'activado' if enable else 'desactivado'}")
            self.client.set_session(alt_speed_enabled=enable)
            logger.debug("Nueva configuración de la sesión aplicada")
            return True
        except Exception as e:
            logger.error(f"Error al cambiar límite de velocidad en Transmission: {str(e)}")
            return False

    def _toggle_synology_ds_speed_limit(self, enable):
        try:
            logger.info(f"Cambiando límite de velocidad en Synology DS Station a: {'activado' if enable else 'desactivado'}")
            # Convertir a True/False explícitamente
            enabled_value = True if enable else False
            self.client.schedule_set_config(enabled=enabled_value)
            logger.debug("Nueva configuración de la sesión aplicada")
            return True
        except Exception as e:
            logger.error(f"Error al cambiar límite de velocidad en Synology DS Station: {str(e)}")
            return False
