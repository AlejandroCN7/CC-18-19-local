## Provisionamiento

---
MV: 51.145.137.107

En este apartado hablaremos del provisionamiento automático de máquinas virtuales a través de [Ansible](https://www.ansible.com/). Entiendo a Ansible como una herramienta software de administración y manejo de máquinas virtuales. En este punto se pretende ir un paso más allá y provisionarlas de las herramientas necesarias para poder proporcionar el servicio web que se pretende en este proyecto. He decidido utilizar Ansible y no otra alternativa debido a que nuestro profesor de Cloud Computing, JJ Melero, decidió hacer un seminario sobre esta herramienta ([enlace al seminario](https://www.youtube.com/watch?v=gFd9aj78_SM&t=1277s)). Este seminario se realizó más o menos en un margen temporal cercano al comienzo de este hito, por lo que me ha resultado de gran utilidad. 

### Mejoras realizadas en el proyecto

En este punto del desarrollo, y antes de entrar en el tema de provisionamiento, se han realizado una serie de mejoras.

Se ha incluido el uso de una base de datos (MongoDB) como un nuevo microservicio añadido ([ver mongoDB.py](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/mongoDB.py)). La forma de desplegar la base de datos ha sido a través de [mlab](https://mlab.com/), sigue la filosofía "Database-as-a-Service". He elegido esto porque hace que no tengamos que preocuparnos del despliegue de la misma. Es una forma de acceder a servicios que proporciona la nube; uno de los objetivos de esta asignatura.

Se han realizado tests acorde al uso de esta base de datos desplegada en mlab. Se puede ver los tests realizados en [test_mongo.py](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/tests/test_mongo.py). Básicamente se comprueba que podemos insertar, eliminar, actualizar, etc, la base de datos desplegada en mlab de forma correcta y cumpliendo con especificaciones funcionales concretas que he decidido diseñar de esa forma. Por ejemplo, que no se pueda insertar dos jugadores con el mismo Nick, ya que lo utilizo como identificador para luego dar el servicio web (los nombres de las rutas ahora corresponden con el Nick de los jugadores).

He tenido que realizar pequeñas [modificaciones en principal.py](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/commit/a758285dfb726f4a80b5ed745ae6e2baa43dc6a1). Como ya he mencionado antes, ahora el nombre de las rutas en el servicio web depende del nick de los jugadores (algo que tiene mayor lógica). Utilizamos directamente la base de datos en lugar de un diccionario de Python para almacenar los datos. Incluida la petición REST DELETE para el conjunto de jugadores (ruta <ip>/jugadores), esto dejaría la base de datos vacía (comprobado en los tests).

Finalmente, se ha [modificado test_web.py](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/commit/6b6dbe458b0f0f52527f0f20cec18076301febfe#diff-b946cfc9c7d6cd8ba6ce887aa8cdcd44), ya que aquí es donde comprobabamos las rutas y peticiones REST de nuestro servicio web. Es importante destacar que estos cambios son realizados a causa de la actualización del nombre de las rutas, no de añadir una base de datos, ya que la idea es que se encuentre de forma aislada en microservicios. En definitiva, se han tenido que cambiar las comprobaciones en las rutas a la hora de realizar las distintas peticiones, simplemente.

### Vagrant

Tal y como se pide en el hito de esta práctica, se han realizado primero pruebas con máquinas virtuales locales para realizar el provisionamiento desde ansible y probarlo en localhost. Para ello he utilizado la herramienta [vagrant](https://www.vagrantup.com/docs/index.html) ya que es una forma muy sencilla de crear máquinas virtuales a través de virtualbox, en mi caso, con el cual ya estaba familiarizado previamente y fue otro de los factores por el que decidí utilizarlo y que explicó JJ en el seminario de Ansible. Los archivos de configuración de Ansible pueden apreciarse en la carpeta [vagrant](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/tree/master/provision/vagrant) dentro de [provision](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/tree/master/provision).

Para comenzar, [ansible.cfg]https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/provision/vagrant/ansible.cfg) es un archivo que hemos creado para que Ansible no utilice su configuración por defecto, sino que vamos a establecer una configuración concreta cuando lo ejecutemos dentro de este subdirectorio. Como estamos trabajando con vagrant, vagrant crea un directorio oculto (.vagrant) en el que guarda información de la máquina virtual. Aquí especificamos que no queremos que se realicen comprobaciones de la clave del host, esto nos permite la posibilidad de meternos en diferentes máquinas virtuales con diferentes nombres y misma dirección MAC, o con el mismo nombre y diferentes MAC, sin que haya ningún problema y no te haga este tipo de comprobación SSH.

La segunda parte del archivo sirve para especificar el inventario. Le decimos a Ansible el archivo en el que se encuentra la información que necesita para saber como conectarse a las distintas máquinas virtuales que tenemos creadas. Este archivo es [ansible_hosts](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/provision/vagrant/ansible_hosts).

En su interior le especificamos una única máquina llamada debian9Vagrant la cual Ansible sabe a partir de este momento que tiene que comunicarse por el puerto 2222. La clave privada para poder conectarse se encuentra dentro de la carpeta oculta de vagrant que mencionamos anteriormente (.vagrant), de lo contrario ansible no sería capaz de acceder a ella para realizar su provisionamiento automático. Finalmente, especificamos en este archivo el host (localhost) y el usuario con el que tiene que acceder a la máquina llamado "vagrant".

De esta forma ansible tiene todo lo necesario para comunicarse y acceder a la máquina virtual que hemos creado, aunque podría ser más de una.

![acceso a la máquina vagrant a través de Ansible](docs/figuras/hito3/vagrant.png)

El siguiente paso es realizar un guión con el que ansible pudiera hacer un provisionamiento automático a la o las máquinas.

Para ellos se utilizan los playbooks, en mi caso he creado [playbook.yml](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/provision/vagrant/playbook.yml) en el cual hacemos básicamente las siguientes acciones dentro de la máquina:

- Instalar git si no se encuentra.
- Instalar herramientas como curl y pip para python3.
- Clonar este repositorio de github (sin permisos de superusuario)
- Instalar dependencias de los servicios que proporcionamos para pip ([requirements.txt](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/requirements.txt))

![Provisionamiento de vagrant con Ansible](docs/figuras/hito3/provisionamiento-vagrant.png)

Mencionar que salen estados OK porque ya lo había ejecutado antes, por lo que ya lo tiene instalado en la máquina y no lo vuelve a hacer, solo lo comprueba.

Una vez hecho esto podemos entrar en la máquina, ejecutar el servicio con gunicorn y comprobar que funciona en localhost, sin embargo veremos su funcionamiento ya desplegado directamente a continuación.

### Azure

Lo interesante de este hito es la posibilidad de desplegar nuestra máquina virtual a través de la herramienta [Azure](https://azure.microsoft.com/es-es/) y de esta forma provisionar con Ansible algo que se encuentra en la nube en ese momento. Esto me resulta muy interesante, por ejemplo, se me ocurre la posibilidad de ejecutar nuevos playbooks mientras la máquina funciona para realizar nuevos cambios, modificar el servicio o sustituirlo por otro.

He elegido Azure para realizar el despliegue de la máquina debido a que JJ nos proporcionó dolares para poder utilizar esta herramienta y quería aprovecharlo.

Lo primero que hay que hacer una vez nos registramos en Azure es crear nuestra máquina virtual "virgen", es decir, sin nada instalado. Para ello he utilizado la propia interfaz de la página. En un principio, había instalado en ella el sistama operativo Debian 9 para servidores. Sinceramente, no lo hice por ningún motivo especial, simplemente porque aun estaba realizando pruebas y fue el primero que se me vino a la cabeza.

Entonces, como se puede ver en el [antiguo estado de playbook.yml para azure](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/commit/1ed355fad1aceef9a691fc4093b10480474b798c) me dió muchos problemas para poder redirigir el puerto 5000 al 80. Y aún así, seguía teniendo problemas con eso. Por ello, decidí cambiarme a Ubuntu Server 16.04 LTS.

Esta vez si me pensé mejor cual era el SO que quería correr en mi máquina virtual. Las principales cuestiones por las que elegí Ubuntu Server es porque estoy familiarizado a su funcionamiento gracias a la asignatura de Ingeniería de Servidores en el Grado en Ingeniería Informática de la Universidad de Granada. Además, es estos sistemas ya tenemos instalado python2 y python3 preinstalado, por lo que nos ahorra parte del trabajo.

El archivo [ansible.cfg](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/provision/azure/ansible.cfg) es igual al explicado anteriormente con Vagrant. El archivo [ansible_hosts](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/provision/azure/ansible_hosts) solo ha sido modificado con el nombre de la máquina de Azure (solo por comodidad, para Ansible no tiene por qué tener el mismo nombre) y con el usuario e IP pública de la misma.

Finalmente se ha creado el [playbook.yml](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/provision/azure/playbook.yml) el cual es muy parecido al explicado con Vagrant pero difiere en algunas cosas. Digamos que instala las dependecias y clona este repositorio de la misma forma que lo hace Vagrant, pero aquí hemos tenido en cuenta la redirección de puertos. De esta forma, se tiene acceso también por el puerto 80 que era uno de los requisitos de este hito.

El siguiente paso ha sido entrar en la carpeta del repositorio [azure](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/tree/master/provision/azure) dentro de [provision](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/tree/master/provision) y ejecutar el playbook para que ansible provisione automáticamente nuestra máquina de Azure.

![Provisionamiento de Azure con Ansible](docs/figuras/hito3/provisionamiento-azure.png)

Una vez realizado el provisionamiento accedí a la máquina virtual de Azure introduciendo:

`ssh Alejandro@51.145.137.107`

Y una vez dentro probé a arrancar el servicio por medio del comando:

`gunicorn -b :5000 principal:app`

Aunque especifique el puerto 5000, como en el provisionamiento se realizó la redirección del puerto debería de estar disponible también en el puerto 80. Lo comprobé accediendo a esa IP con ese puerto por medio del navegador:

![Puesta en marcha del servicio](docs/figuras/hito3/servicio-azure.png)

![Acceso a ruta raíz](docs/figuras/hito3/prueba-azure.png)

![Acceso a ruta jugadores](docs/figuras/hito3/prueba2-azure.png)

Con ello demostramos que el provisionamiento se ha realizado correctamente y que desde ese momento nuesta máquina virtual está lista para poder trabajar y realizar el servicio diseñado hasta la fecha en nuestro proyecto a través de la nube.

### Comprobaciones con otros alumnos

He probado a provisionar una máquina a través del repositorio de @lgaq94. Se puede ver el [pull request](https://github.com/luiisgallego/MII_CC_1819/commit/a26f2501515daf80dba1587316f0a05f8dd9afed) y el [archivo](https://github.com/luiisgallego/MII_CC_1819/blob/master/provision/Prueba_Provision/Prueba_provisionamiento.md).

@lgaq94 a provisionado una máquina a través de mi repositorio haciendo un [pull request](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/commit/c7021616b5e480bf5691ab11be3c09d98058a183) de este [archivo](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/docs/comprobacionProvision.md).
