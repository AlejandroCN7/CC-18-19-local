# Servicio de búsqueda para jugadores de videojuegos

---

**Autor: Alejandro Campoy Nieves**

**Asignatura: Cloud Computing (Máster Profesional en Ingeniería Informática)**

**Universidad: Universidad de Granada (UGR)**

## Descripción del problema

---

Cada vez es más común encontrarse videojuegos en el mercado totalmente centrados
en el modo **online** cooperativo o competitivo con otros jugadores. Los videojuegos
offline o de modo historia siguen teniendo éxito coexistiendo con los
anteriormente mencionados. Es muy común encontrarse con gente que le atrae un
videojuego pero simplemente no puede disfrutarlo al máximo porque no tiene con
quien jugarlo y esto reduce su experiencia como jugador.

Aunque siga habiendo de todo, los juegos online y los [deportes
electrónicos](https://es.wikipedia.org/wiki/Deportes_electr%C3%B3nicos) de jugadores en este
proyecto.

## Descripción de la solución

---

La idea consiste en crear una **plataforma** en la cual puedan **registrarse** los
jugadores de videojuegos especificando sus datos (nombre, edad, plataforma de juego, etc).
Entonces, el jugador en cuestión tendrá la posibilidad de especificar a qué videojuegos
está jugando en la actualidad y con qué frecuencia. A su vez, se desarrollará un
**buscador** de otros perfiles mediante distintos criterios de búsqueda, como un
videojuego en concreto al que esté jugando. Con ello permitiremos que jugadores
con gustos y objetivos similares dentro de un videojuego puedan ponerse en **contacto**
y disfrutar de la experiencia extra que supone degustar un videojuego en compañía.

## Arquitectura

---

Se pretende realizar un despliegue en la nube utilizando para ello una arquitectura basada en
[microservicios](https://www.redhat.com/es/topics/microservices). De esta forma tenemos la posibilidad de dar un servicio grande
presentándolo como un conjunto de pequeños servicios (microservicios) que funcionan
de una forma totalmente independiente (aunque luego se comuniquen y colaboren entre ellos). En función de las necesidades que se han especificado en la descripción de la solución, inicialmente, planteo el desarrollo de los siguientes microservicios:

- Gestión de usuarios (Sing up, log in, modificación del perfil de usuario...).

- Gestión de la base de datos MongoDb.

- Microservicio de búsqueda de jugadores por criterio.

- Microservicio para mostrar la información de una forma determinada.

## Comunicación entre microservicios

---

Tal y como se ha mencionado en clase, la idea es comunicar los microservicios con un broker llamado [RabbitMQ](https://www.rabbitmq.com/).

## Desarrollo

---

El lenguaje que vamos a utilizar para implementar cada uno de los microservicios mencionados anteriormente va a ser, en principio, [Python](https://www.python.org/). Va a ser vinculado a una base de datos no relacional llamada [MongoDB](https://www.mongodb.com/es) a través de [Pymongo](https://api.mongodb.com/python/current/), que es una distribución de Python la cual contiene herramientas para trabajar con esta base de datos. Además, vamos a hacer uso de un framework para desarrollo web llamado [Django](https://www.djangoproject.com/) cuya finalidad es facilitarnos en cierta medida el trabajo de desarrollo.

## Pruebas y test

---

En principio, para realizar un desarrollo basado en pruebas, haremos uso de [doctest](https://docs.python.org/2/library/doctest.html) para Python, aunque no se descarta utilizar algún marco que nos ayude a crearlos en un alto nivel como puede ser [Pocha](https://github.com/rlgomes/pocha) ([Mocha](https://mochajs.org/) para Python).

## Despliegue

---

El despliegue del servivio web se llevará a cabo utilizando [Ansible](https://www.ansible.com/), siguiendo la filosofía de plataforma como un servicio (Paas) en la nube.

## Licencia

---

Este proyecto está bajo la licencia de [GNU GENERAL PUBLIC LICENSE](https://es.wikipedia.org/wiki/GNU_General_Public_License)
