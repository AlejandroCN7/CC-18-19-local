# Esta es la imagen de la cual partimos para hacer la mia propia.
FROM frolvlad/alpine-python3:latest
# He visto que es una forma de especificar el autor.
MAINTAINER Alejandro Campoy

# Con esta imagen se supone que ya tenemos instalado python3 en Alpine

#Indicamos el directorio de trabajo de la imagen:
WORKDIR ~/proyecto/

# Esta variable de entorno será utilizada para indicar que vamos a conectar con MLAB.
ENV MLAB yes

#Copiamos los directorios necesarios para que funcione el servicio web.
COPY ./principal.py  principal.py
COPY ./mongoDB.py  mongoDB.py
COPY ./model.py  model.py
COPY ./requirements.txt requirements.txt

# Esto servirá para abrir el puerto 80
EXPOSE 80

# Instalamos las dependecias del servicio (Flask, Flask_restful, pymongo y gunicorn)
RUN pip3 install -r requirements.txt
# Ejecutamos el servicio
CMD gunicorn -b :80 principal:app
