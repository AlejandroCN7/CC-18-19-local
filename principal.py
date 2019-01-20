from flask import Flask
from flask_restful import Resource, Api, abort, reqparse
from model import Jugador
from mongoDB import BaseDatos
import logging

import os

app = Flask("hito5")
api = Api(app)

#Para el sistema de logs
logging.basicConfig(filename='app.log', filemode='a',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG,  datefmt='%d-%b-%y %H:%M:%S')

# Esto ser?a con flask sin el microframework de RestFul
#@app.route("/")

#def hello():
    #return "Hola Mundo !! :)

# Si se trata de una prueba de travis debe de hacerlo en local
if('TRAVIS' in os.environ):
    mongo = BaseDatos("mongodb://127.0.0.1:27017/MiBaseDatos", True)
else:
    mongo = BaseDatos("mongodb://10.0.0.5:27017/MiBaseDatos",False)

#recursos = {"jugador1":j1.__dict__(),
#            "jugador2":j2.__dict__(),
#            "jugador3":j3.__dict__()
#            }

parser = reqparse.RequestParser()
parser.add_argument('Nick', type=str, help='El nick debe ser ?nico',required = True)
parser.add_argument('Nombre', type=str, required = True)
parser.add_argument('Apellidos', type=str, required = True)
parser.add_argument('Edad', type=int, required = True)
parser.add_argument('Videojuegos', required = True, action="append")
parser.add_argument('Competitivo', type=str, required = True)


def abortar_ruta_inexistente(ruta):
    for j in mongo.jugadores.find():
        if(ruta == j['Nick']):
            return
    abort(404, message="Error 404. La ruta {} no existe".format(ruta))

class Principal(Resource):
    def get(self):
        return {'status':'OK'}

class JugadorIndividual(Resource):

    def get(self,ruta):
        abortar_ruta_inexistente(ruta)
        logging.info("Obteniendo jugador de la base de datos.")
        return {ruta:mongo.getJugador(ruta)}

    def put(self,ruta):
        args = parser.parse_args()
        jugador = Jugador(args['Nick'], args['Nombre'], args['Apellidos'], args['Edad'],
                          args['Videojuegos'], args['Competitivo'])
        exito = mongo.insertJugador(jugador)
        if(not(exito)):
            mongo.updateJugador(args['Nick'],jugador.__dict__())
        return mongo.getJugador(ruta)

    def delete(self,ruta):
        mongo.removeJugador(ruta)
        return '',204

class Jugadores(Resource):

    def get(self):
        return mongo.getJugadores()

    def post(self):
        args = parser.parse_args()
        jugador = Jugador(args['Nick'], args['Nombre'], args['Apellidos'], args['Edad'],
                          args['Videojuegos'], args['Competitivo'])
        ruta = args['Nick']
        mongo.insertJugador(jugador)
        return mongo.getJugador(ruta),201

    def delete(self):
        mongo.removeJugadores()
        return '',204

api.add_resource(Principal,'/','/principal')
api.add_resource(Jugadores,'/jugadores')
api.add_resource(JugadorIndividual,'/jugadores/<string:ruta>')


if (__name__ == '__main__'):
    # Esto es para que pueda abrirse desde cualquier puerto y direccion(de esta forma en heroku no nos da error).
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port,debug=False)
    #app.run(debug=True)
