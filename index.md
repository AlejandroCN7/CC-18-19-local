# Servicio de búsqueda para jugadores de videojuegos

## Descripción del problema

Cada vez es más común encontrarse videojuegos en el mercado totalmente centrados
en el modo **online** cooperativo o competitivo con otros jugadores. Los videojuegos
offline o de modo historia siguen teniendo éxito coexistiendo con los
anteriormente mencionados. Es muy común encontrarse con gente que le atrae un
videojuego pero simplemente no puede disfrutarlo al máximo porque no tiene con
quien jugarlo y esto reduce su experiencia como jugador.

Aunque siga habiendo de todo, los juegos online y los deportes
electrónicos se han ido poniendo de moda en los últimos años. Por consiguiente,
se ha planteado dar un servicio específico para este tipo de jugadores en este
proyecto.

## Descripción de la solución

La idea consiste en crear una **plataforma** en la cual puedan **registrarse** los
jugadores de videojuegos especificando sus datos (nombre, edad, plataforma de juego, etc).
Entonces, el jugador en cuestión tendrá la posibilidad de especificar a qué videojuegos
está jugando en la actualidad y con qué frecuencia. A su vez, se desarrollará un
**buscador** de otros perfiles mediante distintos criterios de búsqueda, como un
videojuego en concreto al que esté jugando. Con ello permitiremos que jugadores
con gustos y objetivos similares dentro de un videojuego puedan ponerse en **contacto**
y disfrutar de la experiencia extra que supone degustar un videojuego en compañía.

## Arquitectura

Se pretende realizar un despliegue en la nube utilizando para ello una arquitectura basada en
microservicios. De esta forma tenemos la psibilidad de dar un servicio grande
presentándolo como un conjunto de pequeños servicios (microservicios) que funcionan
de una forma totalmente independiente.

El proyecto se realizará utilizando esencialmente como lenguaje de programación
Python.
