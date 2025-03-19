# SPEED-PLAY-PLEX

Control de velocidad alternativa de clientes torrent basado en la actividad de Plex (API Tautulli).

Imaginemos que tenemos compartiendo todas las imágenes de Linux que hay disponibles de todas las distribuciones en todas sus versiones, eso nos ocupa un ancho de banda importante y nos vamos a casa de unos amigos y queremos conectarnos a nuestro Plex para enseñarles nuestro último documental en Zimbabue de los rinocerontes blancos del sur grabado con nuestra flamante nueva cámara de vídeo en 8K y tenemos el problema que se nos corta la emisión por el ancho de banda ocupado, con este docker podemos controlar cuando hay una reproducción en nuestro Plex y así limitar la velocidad de subida y bajada de nuestras distribuciones de Linux compartidas con los amantes de OpenSource.   

Requerimientos para utilizar este contenedor:

- Utilizar **Tautulli** como aplicación de monitoreo de la actividad de Plex Media Server.
- Utilizar como cliente de torrents: **qBittorrent, Transmission, Synology Download Station, rTorrent o Deluge.**

### Configuración variables de entorno en fichero .env (renombrar el env-example a .env)

| VARIABLE                 | NECESARIA | VERSIÓN | VALOR |
|:------------------------ |:---------:| :------:| :-------------|
| TAUTULLI_IP              |     ✅    | v1.0.0  | Host/IP del servicio de Tautulli. Ejemplo: 192.168.2.20                             |
| TAUTULLI_PORT            |     ✅    | v1.0.0  | PUERTO del servicio de Tautulli. Ejemplo: 8182                                      |
| TAUTULLI_API_KEY         |     ✅    | v1.0.0  | Nuestra API key generada en Tautulli en Settings -> Web Interface.                  |
| CLIENTE_TORRENT          |     ✅    | v1.5.0  | Cliente de descarga de Torrents. (qbittorrent, transmission, synology_ds, rtorrent o deluge) |
| CLIENTE_TORRENT_IP       |     ✅    | v1.0.0  | Host/IP del cliente Torrent. Ejemplo: 192.168.2.20                                  |
| CLIENTE_TORRENT_PORT     |     ✅    | v1.0.0  | Puerto del cliente Torrent. Ejemplo: 8090                                           |
| CLIENTE_TORRENT_USER     |     ✅    | v1.0.0  | Usuario del cliente Torrent.                                                        |
| CLIENTE_TORRENT_PASSWORD |     ✅    | v1.0.0  | Contraseña del cliente Torrent.                                                     |
| VEL_ALTERNATIVA_DESCARGA |     ✅    | v1.5.0  | Velocidad de descarga solo para la opción de cliente rTorrent y Deluge (en MB/s.)            |
| VEL_ALTERNATIVA_SUBIDA   |     ✅    | v1.5.0  | Velocidad de subida solo para la opción de cliente rTorrent y Deluge (en MB/s.)              |
| ENDPOINT_RTORRENT        |     ✅    | v1.4.0  | Solo para rTorrent, parte del ENDPOINT. visita https://github.com/unraiders/speed-play-plex/releases/tag/v1.4.0 para más info. |
| DEBUG                    |     ✅    | v1.2.0  | Habilita el modo Debug en el log. (0 = No / 1 = Si)                                 |
| TZ                       |     ✅    | v1.1.0  | Timezone (Por ejemplo: Europe/Madrid)                                               |

La VERSIÓN indica cuando se añadió esa variable o cuando sufrió alguna actualización. Consultar https://github.com/unraiders/speed-play-plex/releases

---

### Ejemplo docker-compose.yml (con fichero .env aparte)
```yaml
services:
  speed-play-plex:
    image: unraiders/speed-play-plex
    container_name: speed-play-plex
    restart: unless-stopped
    network_mode: bridge
    env_file:
      - .env
    ports:
      - "9898:9898"
```

---

### Ejemplo docker-compose.yml (con variables incorporadas)
```yaml
services:
  speed-play-plex:
    image: unraiders/speed-play-plex
    container_name: speed-play-plex
    restart: unless-stopped
    network_mode: bridge
    environment:
        - TAUTULLI_IP=
        - TAUTULLI_PORT=
        - TAUTULLI_API_KEY=
        - CLIENTE_TORRENT=  # Opciones: qbittorrent, transmission, synology_ds, rtorrent o deluge
        - CLIENTE_TORRENT_IP=
        - CLIENTE_TORRENT_PORT=
        - CLIENTE_TORRENT_USER=
        - CLIENTE_TORRENT_PASSWORD=
        - VEL_ALTERNATIVA_DESCARGA=
        - VEL_ALTERNATIVA_SUBIDA=
        - ENDPOINT_RTORRENT=
        - DEBUG=0
        - TZ=Europe/Madrid
    ports:
        - "9898:9898"       
```

---

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

---

  > [!TIP]
  > Podemos crear tantos webhooks como queramos, imaginemos que tenemos 3 clientes torrents funcionando en nuestro sistema y
  > queremos controlar la velocidad alternativa en los 3, pues creamos 3 webhooks a los que la única diferencia será el puerto
  > de destino a especificar que se corresponderá con el puerto expuesto que hayamos definido en cada uno de los contenedores de 
  > speed-play-plex.

---

  > [!TIP]
  > Funcionando en:
  >  - Tautulli v2.15.1
  >  - qBittorrent v4.6.6
  >  - Transmission v4.0.5
  >  - Synology Download Station 4.0.3-4720
  >  - rTorrent 0.9.8
  >  - Deluge 2.1.1
  >  - Es posible que funcione en versiones anteriores y posteriores de estos clientes.

---

### Configuración velocidad alternativa en clientes torrents.

- **qBittorrent**: Click en rueda dentada del menú superior, pestaña "Speed" -> "Alternative Rate Limits".
- **Transmission**: Click en rueda dentada del menú superior, pestaña "Speed" -> "Alternative Rate Limits".
- **Synology Download Station**: En el cliente Synology Download Station tenemos que hacer un paso adicional que es definir un Plan de programa, hacemos click a la rueda dentada en la parte inferior izquierda de nuestro cliente de torrent, en la sección BT/HTTP/FTP/NZB nos vamos a General y en Programa de descargas -> Programa avanzado y click en el botón "Plan de programa", aquí seleccionamos "Velocidad alternativa de BT" haciendo click en el cuadrado naranja, ahora arrastramos el ratón por toda la franja de días y horarios del cuadro inferior y se nos tiene que marcar todo en color naranja, por último indicamos cual será nuestra velocidad máxima de carga y descarga cuando tengamos una reproducción en Plex, ya está click en el botón "OK" y muy importante en "Programa de descargas" seleccionar "Inmediatamente" y click en botón "OK".
- **rTorrent**: En el caso de rTorrent al no disponer de opción de velocidad alternativa dentro de su configuración utilizaremos las variables de entorno VEL_ALTERNATIVA_DESCARGA y VEL_ALTERNATIVA_SUBIDA para indicarle cual será la velocidad en el caso de que exista una reproducción en Plex.
- **Deluge**: En el caso de Deluge al no disponer de opción de velocidad alternativa dentro de su configuración utilizaremos las variables de entorno VEL_ALTERNATIVA_DESCARGA y VEL_ALTERNATIVA_SUBIDA para indicarle cual será la velocidad en el caso de que exista una reproducción en Plex.   

- Podemos calcular la velocidad deseada en está página: https://www.calculator.net/bandwidth-calculator.html

---

### Peculiaridades rTorrent.

- Este cliente de torrent se puede encontrar con imágenes creadas por diferentes mantenedores y en cada una podemos encontrar que el puerto para la comunicación XMLRPC con el cliente sea diferente, por ejemplo:

-  Imagen oficial [rakshasa/rtorrent](https://github.com/rakshasa/rtorrent) el puerto interno que expone XMLRPC es el 5000.
-  Otra imagen [crazy-max/docker-rtorrent-rutorrent](https://github.com/crazy-max/docker-rtorrent-rutorrent) el puerto que expone XMLRPC es el 8000. (con esa imagen la autenticación está deshabilitada por defecto, podemos dejar las variables de usuario y contraseña vacías, en el caso de querer activar la autenticación en el repositorio está en procedimiento).
- Imagen de hotio que integra flood con rTorrent [ghcr.io/hotio/rflood](https://hotio.dev/containers/rflood) el puerto que expone XMLRPC es el 5000. (si ya tenemos corriendo esta imagen con anterioridad, leer la página de hotio que indica como sacar el usuario y contraseña para la conexión).
- A partir de la versión v1.4.0 del contenedor se separa de la URL el ENDPOINT y se pasa como variable (ENDPOINT_RTORRENT), dado que dependiendo de la versión de rTorrent y de los plugins instalados puede cambiar el ENDPOINT de la URL. Los ENDPOINT mas usuales son: /RPC2 o /plugins/rpc/rpc.php o /plugins/httprpc/action.php 

---

### Peculiaridades Deluge.

- En el caso de Deluge nos tenemos que asegurar que el contenedor de Deluge expone el puerto 58846 (puerto utilizado para la comunicación con el cliente).

---

### Instalación plantilla en Unraid.

- Nos vamos a una ventana de terminal en nuestro Unraid, pegamos esta línea y enter:
```sh
wget -O /boot/config/plugins/dockerMan/templates-user/my-speed-play-plex.xml https://raw.githubusercontent.com/unraiders/speed-play-plex/refs/heads/main/my-speed-play-plex.xml
```
- Nos vamos a DOCKER y abajo a la izquierda tenemos el botón "AGREGAR CONTENEDOR" hacemos click y en seleccionar plantilla seleccionamos speed-play-plex y rellenamos las variables de entorno necesarias, tienes una explicación en cada variable en la propia plantilla.
