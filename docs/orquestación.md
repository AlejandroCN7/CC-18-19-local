## Orquestación

---
Despliegue Vagrant: mv.servicioclo.ud

En este hito vamos a hablar sobre la orquestación de dos máquinas virtuales para poner en funcionamiento nuestro conjunto de microservicios. Para ello, haremos uso una vez más de [Azure](https://azure.microsoft.com/es-es/), pero esta vez, utilizando [Vagrant](https://www.vagrantup.com/) para este proceso de orquestación anteriormente mencionado. Hasta este momento, solo hacía uso de una máquina virtual, por lo que he tenido que ampliar el proyecto para tener la posibilidad de utilizar, al menos, dos máquinas virtuales y que este trabajo tenga sentido a nivel de infraestructura, hablaremos de esto en mayor detalle posteriormente. También se ha realizado pruebas de orquestación a otra alumna y ella ha realizado una prueba de orquestación con mi proyecto.

### Mejoras realizadas en el proyectos

#### Máquinas virtuales

Como ya he mencionado anteriormente, era imprescindible que para este hito tuviese, al menos, dos máquinas virtuales con las que poder trabajar en mi servicio. Por ello, abandoné [mlab](https://mlab.com/) y he configurado mi propia máquina virtual en la que doy un servicio con [MongoDB](https://www.mongodb.com/es). Decidí esta base de datos (desde que usaba mlab) porque no había trabajado antes con bases de datos no relacionales, y quería salir un poco de mi zona de confort.

El sistema operativo que decidí para esto fue Ubuntu Server 16.04 LTS. El principal motivo, es que encontré un rol de Ansible que funcionaba perfectamente para la provisión de la máquina con este SO. Probé algunos roles más para otros SO's, pero siempre acababa teniendo algunos problemas de configuración y éste fue el que mejor se adaptaba a mis necesidades. Por otra parte, encontré artículos en los que se menciona que esta sistema operativo es muy adecuado tales como: [este](https://www.quora.com/Which-is-the-best-operating-system-for-MongoDB-and-Hadoop), [este otro](https://www.percona.com/blog/2017/07/19/blog-poll-what-operating-system-do-you-run-your-development-database-on/) y [también este](https://docs.mongodb.com/manual/administration/production-notes/). El último enlace pertenece a la página oficial de MongoDB y se puede apreciar como Ubuntu Server 16.04 LTS tiene una cobertura de soporte total, un factor positivo a tener muy en cuenta, ya que durante la configuración tuve problemas que pude resolver gracias a su documentación y comunidad.

Sin embargo, tuve que modificar el [rol de Ansible](https://github.com/Ilyes512/ansible-role-mongodb) que utilicé para poder instalar MongoDB. La causa era que, por defecto, este rol escribía en /etc/mongod.conf la línea `bindIp: 0.0.0.0`. Esto es algo peligroso, ya que le abro la puerta a todo Internet para que pueda acceder a mi base de datos. Por ello, entre en [este archivo del rol](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/orquestacion/roles/ilyes512.mongodb/tasks/main.yml) y modifiqué esa tarea para que pusiera en su lugar `bindIp: 127.0.0.1,10.0.0.5`. De esta forma, solo puede ser accedida por localhost desde la propia máquina y por a otra máquina con el servicio REST que comparten una misma subnet virtual (hablaremos con mayor detalle de ésto más adelante).

En cuanto al servicio REST utilizamos la misma máquina que el [hito anterior](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/docs/automatizaci%C3%B3n.md).

#### Tests y Travis

En hitos anteriores utilizaba la misma base de datos de mlab con diferentes colecciones para dar tanto el servicio como realizar los tests y verificar que todo funcionaba correctamente. Como ahora tengo la base de datos desplegada por mi propia cuenta, es posible que cuando actualice el repositorio no tenga la máquina levantada. Travis, al no tener el servicio de la base de datos, fallará en sus tests (no me paré a pensar en ello hasta que me sucedió).

La solución que propongo en este proyecto es la instalación local de MongoDB en Travis junto con una variable de entorno para que el servicio de flask sepa diferenciar cuando se trata de una prueba (utilizaría una base de datos local) y cuando se está levantando en Azure. Dejo un enlace por si se quiere consultar los [cambios a .travis.yml](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/commit/ccd3f424aa219fea07c01c46eddd7821998fa39b).

Después simplemente tuve que [modificar principal.py](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/commit/a74ebdda0d599c400dca0510876cecc066d49e38) para que tuviera en cuenta esta variable de entorno. Monta la conexión con la base de datos en local o no dependiendo de si lo está haciendo Travis o no.

#### Correción de errores de hitos anteriores marcados por JJ Melero

He corregido los errores que me indicó JJ Melero en el hito anterior:

- Ya no meto en la misma app los jugadores que voy a usar. Eso ha sido eliminado de [principal.py](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/commit/a74ebdda0d599c400dca0510876cecc066d49e38) y he creado, a parte, [mongoDB_config.py](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/mongoDB_config.py). Este archivo crea una conexión con la base de datos desplegada en Azure y la inicializa con una colección simple de tres jugadores. Simplemente ejecutando esto podemos tener algo en la base de datos para poder hacer pruebas.

- Ya no aparece ninguna clave de ningún tipo en el repositorio. La primera solución que propuse fue crearme una variable de entorno con la contraseña localmente en mi PC. Después, tal y como se refleja en el [playbook.yml](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/orquestacion/playbook.yml), pasaría el valor de esta variable de entorno a una variable de entorno con el mismo nombre en la máquina a provisionar. De esta forma solo aparece el nombre de la variable, pero no su contenido (para ver el contenido habría que; o bien acceder al .bashrc de mi ordenador personal o bien acceder por SSH a la máquina y hacer lo mismo. Cosas que en principio son imposibles que haga alguien que no sea yo). Luego simplemente debía de poner en el código `mongo = BaseDatos("mongodb://alejandro:" + os.environ['MONGOPASS'] + "@10.0.0.5:27017/MiBaseDatos")`. Esto me funcionaba perfectamente, pero como después capé la conexión de la base de datos solo a localhost y al interior de su propia subnet, dejé que simplemente se pudiera entrar sin necesidad de usuario y contraseña, por lo que solo es necesaria la IP y puerto.

- He [actualizado el .gitignore](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/.gitignore) de tal forma que queden fuera del repositorio los playbooks con extensión .retry.

### Orquestación con Vagrant, Azure y Ansible

Vamos a pasar a explicar el hito como tal. Para empezar, nos creamos la carpeta llamada [orquestacion](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/tree/master/orquestacion) en la que hemos creado el [Vagrantfile](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/orquestacion/Vagrantfile). Para realizar la orquestación me he basado en [este enlace](https://github.com/Azure/vagrant-azure) principalmente y en [este otro](https://blog.scottlowe.org/2017/12/11/using-vagrant-with-azure/) aunque en menor medida.

En este archivo utilizamos vagrant-azure para poder trabajar con Azure desde Vagrant. Lo primero que indicamos es donde se encuentra nuestra clave privada de tal forma que podremos conectarnos con todas las máquinas creadas utilizando la misma sin necesidad de contraseñas. El siguiente paso es definir las dos máquinas con las que vamos a trabajar.

#### Máquina para el servicio REST

La máquina es identificada desde Vagrant con el nombre de "rest", aunque el nombre real de la máquina ha sido configurado como "ubuntu16". Seleccionamos como proveedor a Azure para poder utilizarlo y cargamos nuestras variables de entorno definidas previamente para que el proveedor tenga todos los datos necesarios de nuestra cuenta Azure. La metodología para la obtención de los datos viene correctamente explicados en las referencias que he facilitado, simplemente he tenido que crearme variables de entorno en mi .bashrc con esos datos.

Después he realizado la configuración de parámetros de la máquina virtual, he establecido:

- Nombre de la máquina.
- Size (mismo criterio que el [hito anterior](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/docs/automatizaci%C3%B3n.md)).
- Imagen que utiliza.
- Nombre del grupo de recursos.
- Región del grupo de recursos.
- Usuario para la máquina.
- Establecimiento de una red privada.
- Apertura de puertos necesarios.

Aquí podría darse por finalizada la configuración de la primera máquina. Pero no podemos olvidar su provisionamiento correspondiente. Desde Vagrant también tenemos la posibilidad de hacer una provisión con el uso de Ansible y llamar al playbook que corresponda a la máquina. De esta forma volvemos a reutilizar una vez más el trabajo realizado en el hito de provisión de máquinas.

Para conectarnos a la máquina después de haber sido creada solo hay que hacer:

`> vagrant ssh rest`

#### Máquina para el servicio de mongoDB

El proceso es muy similar al de la máquina anterior. Por ello creo que lo más importante a destacar es que, si indicamos el mismo nombre de recursos y mismo nombre de red virtual, esto no sgnifica que cada una tenga una red y grupo de recursos distintas con el mismo nombre. Lo que quiere decir, es que ambas máquinas van a compartirlas. tal y como se puede apreciar en la siguiente imagen:

![subnet](figuras/hito5/subnet.png)

Para conectarnos a la máquina después de haber sido creada solo hay que hacer:

`> vagrant ssh mongo`

### Prueba del correcto funcionamiento del proceso de orquestación

Considero que @andreamorgar ha hecho un buen trabajo de prueba con mi proyecto. Los resultados obtenidos junto con las capturas del proceso se pueden ver [aquí](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/docs/comprobacionOrquestacion.md).

Simplemente destacar que en Vagrant debe de crearse primero una máquina y después otra (secuencialmente) para que la configuración de la subnet y del grupo de recursos se haga correctamente. Vagrant, por defecto, lo hace en paralelo y produce problemas como asignaciones de la misma IP (supongo que porque creara dos subnets, en lugar de una y que este compartida por ambas máquinas). Le doy las gracias a [Luis Gallego Quero](https://github.com/luiisgallego) por avisarme de este problema antes de toparme con él, ya que a simple vista no es apreciable. Para solucionarlo es importante iniciar el proceso de la siguiente forma:

`> vagrant up --no-parallel --provider=azure`

### Comprobaciones con otros alumnos

He probado a orquestar dos máquinas a través del repositorio de @andreamorgar. Se puede ver el [pull request](https://github.com/andreamorgar/ProyectoCC/commit/4916375107e49678e164356f42cbeb76fed0e913) y el [archivo](https://github.com/andreamorgar/ProyectoCC/blob/master/docs/Prueba-Orquestaci%C3%B3n-%20Alejandro_Campoy_Nieves.md).

@andreamorgar a orquestado mi proyecto a través de mi repositorio haciendo un [pull request](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/commit/f05759883460631cdf67e1a5001f842bbe47f679) de este [archivo](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/docs/comprobacionOrquestacion.md).
