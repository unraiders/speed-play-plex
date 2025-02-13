# speed-play-plex

Control de velocidad alternativa de clientes torrent basado en la actividad de Plex (API Tautulli).

Requerimientos para utilizar este contenedor:

- Utilizar Tautulli.
- Utilizar como cliente de torrents, qBittorrent o Transmission.

## Configuración variables de entorno.

| CLAVE                   | NECESARIO | VALOR                                                                     |
| :---------------------- | :-------: | :------------------------------------------------------------------------ |
| TAUTULLI_API_KEY        |     ✅    | Nuestra API generada en Tautulli en Settings -> Web Interface.            |
| TAUTULLI_IP             |     ✅    | IP del servicio de Tautulli, ejemplo: 192.168.2.20                        |
| TAUTULLI_PORT           |     ✅    | PUERTO del servicio de Tautulli, ejemplo: 8182                            |
| CLIENTE_TORRENT         |     ✅    | Seleccionar entre qbittorrent o transmission.                             |
| CLIENTE_TORRENT_IP      |     ✅    | IP del cliente de Torrent, ejemplo: 192.168.2.20                          |
| CLIENTE_TORRENT_PORT    |     ✅    | PUERTO del cliente de Torrent, ejemplo: 8090                              |
| CLIENTE_TORRENT_USER    |     ✅    | Usuario en nuestro cliente de Torrent.                                    |
| CLIENTE_TORRENT_PASSWORD|     ✅    | Password en nuestro cliente de Torrent.                                   |
| DEBUG                   |     ✅    | Habilita el modo Debug en el log. (0 = No / 1 = Si)                       |



  > [!IMPORTANT]
  > Este contenedor expone el puerto interno 9898 para recibir el webhook de Tautulli para identificar los estados de "play" y "stop" de las reproducciones de nuestro servidor Plex. 
  > 
  > Por ese motivo requiere de configuración adicional en Tautulli que se detalla a continuación.
  > 


### Configuración Agente de Notificación en Tautulli.

- En Tautulli nos dirigimos a Settings -> Notification Agents.
- Hacemos click en "Add a Notification Agent".
- Seleccionamos Webhook.
- en Webhook URL ponemos en este formato la IP de nuestro contenedor, el PUERTO local que expone, seguido de /webhook.  ejemplo: http://192.168.6.19:9898/webhook
- en Webhook Method lo dejamos en POST y le ponemos la descripción que queramos.
- Nos vamos a la pestaña "Triggers" y seleccionamos "Playback Start" y "Playback Stop".
- Nos vamos a la pestaña "Data" seleccionamos "Playback Start" y en "JSON Data" colocamos lo siguiente:

  ```yaml
  {
    "evento": "{action}",
    "streams": "{streams}",
    "título": "{title}",
    "usuario": "{user}"
  }
  ```
- Nos vamos a la pestaña "Data" seleccionamos "Playback Stop" y en "JSON Data" colocamos lo siguiente:

  ```yaml
  {
    "evento": "{action}",
    "streams": "{streams}",
    "título": "{title}",
    "usuario": "{user}"
  }
  ```
- Ya está todo, le damos "Save" para guardar los cambios. 

### Instalación plantilla en Unraid.

- Nos vamos a una ventana de terminal en nuestro Unraid, pegamos esta línea y enter:
```sh
wget -O /boot/config/plugins/dockerMan/templates-user/my-speed-play-plex.xml https://raw.githubusercontent.com/unraiders/speed-play-plex/refs/heads/main/my-speed-play-plex.xml
```
- Nos vamos a DOCKER y abajo a la izquierda tenemos el botón "AGREGAR CONTENEDOR" hacemos click y en seleccionar plantilla seleccionamos speed-play-plex y rellenamos las variables de entorno necesarias, tienes una explicación en cada variable en la propia plantilla.
