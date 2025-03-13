import requests
from flask import Flask, jsonify, request

from config import TAUTULLI_API_KEY, TAUTULLI_IP, TAUTULLI_PORT
from torrent_controller import TorrentController
from utils import setup_logger

logger = setup_logger(__name__)

def check_active_streams():
    try:
        url = f"http://{TAUTULLI_IP}:{TAUTULLI_PORT}/api/v2"
        params = {
            'apikey': TAUTULLI_API_KEY,
            'cmd': 'get_activity'
        }

        logger.debug("Comprobando streams activos en Tautulli...")
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if data.get('response', {}).get('result') == 'success':
                # Asegurarnos de que streams_count sea un entero
                try:
                    streams_count = int(data.get('response', {}).get('data', {}).get('stream_count', 0))
                except (ValueError, TypeError):
                    streams_count = 0
                logger.info(f"Streams activos encontrados en Tautulli: {streams_count}")
                return streams_count
            else:
                logger.error("Error en la respuesta de Tautulli")
                return 0
        else:
            logger.error(f"Error al conectar con Tautulli: {response.status_code}")
            return 0

    except Exception as e:
        logger.error(f"Error al comprobar streams activos: {str(e)}")
        return 0

def create_app():
    torrent_controller = TorrentController()
    if not torrent_controller.connect():
        raise Exception("No se pudo conectar al cliente torrent")

    # Comprobar streams activos en Tautulli al iniciar el contenedor
    active_streams = check_active_streams()
    if active_streams > 0:
        logger.info(f"Se encontraron {active_streams} streams activos al iniciar - Activando límite de velocidad")
        torrent_controller.toggle_speed_limit(True)
    elif active_streams == 0:
        logger.info("No se encontraron streams activos al iniciar - Desactivando límite de velocidad")
        torrent_controller.toggle_speed_limit(False)

    app = Flask(__name__)

    @app.route('/webhook', methods=['POST'])
    def handle_webhook():
        try:
            data = request.json
            if not data:
                return jsonify({"error": "No data received"}), 400

            evento = data.get('evento', '')
            # Convertimos streams a int, con valor por defecto 0 si no es válido
            try:
                streams = int(data.get('streams', 0))
            except (ValueError, TypeError):
                streams = 0

            logger.debug(f"Webhook recibido: {evento}")
            logger.debug(f"Payload completo: {data}")
            logger.info(f"Streams activos: {streams}")

            if evento == 'play' and streams == 1:
                logger.info("Primera reproducción activa - Activando límite de velocidad")
                torrent_controller.toggle_speed_limit(True)

            elif evento == 'stop':
                if streams == 0:
                    logger.info("No quedan reproducciones activas - Desactivando límite de velocidad")
                    torrent_controller.toggle_speed_limit(False)
                else:
                    logger.info(f"Aún quedan {streams} reproducciones activas - Manteniendo límite de velocidad")

            return jsonify({
                "status": "success",
                "evento": evento,
                "active_streams": streams
            }), 200

        except Exception as e:
            logger.error(f"Error procesando webhook: {str(e)}")
            return jsonify({"error": str(e)}), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9898)
