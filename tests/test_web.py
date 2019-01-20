import sys
sys.path.append("../")

import unittest
from model import Jugador
from mongoDB import BaseDatos
from principal import *
import json

#Obtenemos el diccionario de python a partir del contenido expresado en JSON
def obtenerContenidoPaquete(respuesta):
    contenido = respuesta.data.decode('utf8').replace("'", '"')
    return json.loads(contenido)


class TestModel(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

        #Inicializamos la base de datos de prueba con unos jugadores de ejemplo
        mongo = BaseDatos("mongodb://127.0.0.1:27017/MiBaseDatos", True)
        j1 = Jugador("Hapneck", "Alejandro", "Campoy Nieves", 22, ["Fortnite", "Hollow Knight", "The Witcher"], True)
        j2 = Jugador("Malcaide", "Alfonso", "Barragan Lara", 22, ["Counter Strike"], True)
        j3 = Jugador("Rekkles", "Juan", "Martinez Casado", 22, ["Fortnite", "League of Legends", "Counter Strike"],False)

        mongo.insertJugador(j1)
        mongo.insertJugador(j2)
        mongo.insertJugador(j3)

    # respuesta.headers para consultar el tipo MIME del contenido
    # respuesta.status_code para saber el código de la cabecera de respuesta.
    def test1GetRaiz(self):
        
        respuesta = self.app.get('/')

        self.assertEqual(respuesta.status_code,200,"El servidor no se encuentra levantado.")
        self.assertEqual(respuesta.headers['content-type'],'application/json',"Tipo MIME de la cabecera no es JSON.")
        contenido = obtenerContenidoPaquete(respuesta)
        self.assertEqual(contenido['status'],"OK","El contenido de la raíz no es correcta.")

        

    def test2GetPrincipal(self):

        respuesta = self.app.get('/principal')

        self.assertEqual(respuesta.status_code, 200, "El servidor no se encuentra levantado.")
        self.assertEqual(respuesta.headers['content-type'], 'application/json', "Tipo MIME de la cabecera no es JSON.")
        contenido = obtenerContenidoPaquete(respuesta)
        self.assertEqual(contenido['status'], "OK", "El contenido de la raíz no es correcta.")
        
    def test3Error404(self):

        respuesta = self.app.get('/rutaInexistente')
        self.assertEqual(respuesta.status_code,404,"El servidor no muestra correctamente el estado de un recurso no encontrado (404), muestra en su lugar el código " + str(respuesta.status_code) + ".")


    def test4GetJugadores(self):

        respuesta = self.app.get('/jugadores')
        self.assertEqual(respuesta.status_code, 200, "El recurso de jugadores no se encuentra disponible.")
        self.assertEqual(respuesta.headers['content-type'], 'application/json', "Tipo MIME de la cabecera no es JSON.")
        contenido = obtenerContenidoPaquete(respuesta)
        jugadores = contenido.keys()
        self.assertIn('Hapneck',jugadores,"Hapneck no se encuentra disponible.")
        self.assertIn('Malcaide', jugadores, "Malcaide 2 no se encuentra disponible.")
        self.assertIn('Rekkles', jugadores, "Rekkles 3 no se encuentra disponible.")


    def test5PostJugadores(self):

        respuesta = self.app.get('/jugadores')
        self.assertEqual(respuesta.status_code, 200, "El recurso de jugadores no se encuentra disponible.")
        self.assertEqual(respuesta.headers['content-type'], 'application/json', "Tipo MIME de la cabecera no es JSON.")
        contenido = obtenerContenidoPaquete(respuesta)
        self.assertEqual(len(contenido.keys()),3,"Número de jugadores debería ser 3 en este punto.")

        respuesta = self.app.post('/jugadores',data = Jugador("EjemploPost", "Alberto", "Soriano Martinez", 15, ["juego1", "juego2", "juego3"], True).__dict__())
        contenido = obtenerContenidoPaquete(respuesta)
        self.assertEqual(respuesta.status_code, 201, "El recurso no se ha añadido correctamente con post.")
        self.assertEqual(respuesta.headers['content-type'], 'application/json', "Tipo MIME de la cabecera no es JSON.")
        self.assertEqual(contenido['Nick'],"EjemploPost","Parece que POST no ha añadido el jugador de la forma correcta.")

        respuesta = self.app.get('/jugadores')
        self.assertEqual(respuesta.status_code, 200, "El recurso de jugadores no se encuentra disponible.")
        self.assertEqual(respuesta.headers['content-type'], 'application/json', "Tipo MIME de la cabecera no es JSON.")
        contenido = obtenerContenidoPaquete(respuesta)
        self.assertEqual(len(contenido.keys()), 4, "Número de jugadores debería de ser 4 después de haber realizado un POST.")
        self.assertEqual(contenido['EjemploPost']['Edad'], 15, "Parece que el nuevo jugador no ha sido creado correctamente.")

    def test6GetJugador(self):

        respuesta = self.app.get('/jugadores/Hapneck')
        self.assertEqual(respuesta.status_code, 200, "El recurso Hapneck no se encuentra disponible." )
        self.assertEqual(respuesta.headers['content-type'], 'application/json', "Tipo MIME de la cabecera no es JSON.")
        contenido = obtenerContenidoPaquete(respuesta)
        self.assertEqual(contenido['Hapneck']['Nick'],"Hapneck","El nick del jugador no se corresponde con el recurso.")

    def test7DeleteJugador(self):

        respuesta = self.app.get('/jugadores')
        self.assertEqual(respuesta.status_code, 200, "El recurso de jugadores no se encuentra disponible.")
        self.assertEqual(respuesta.headers['content-type'], 'application/json', "Tipo MIME de la cabecera no es JSON.")
        contenido = obtenerContenidoPaquete(respuesta)
        self.assertEqual(len(contenido.keys()), 4, "Debe haber 4 jugadores en este punto.")

        respuesta = self.app.get('/jugadores/EjemploPost')
        self.assertEqual(respuesta.status_code, 200, "El recurso de jugadores no se encuentra disponible.")
        self.assertEqual(respuesta.headers['content-type'], 'application/json', "Tipo MIME de la cabecera no es JSON.")
        contenido = obtenerContenidoPaquete(respuesta)
        self.assertEqual(contenido['EjemploPost']['Nick'],"EjemploPost", "El cuarto jugador no es el que se esperaba")

        respuesta = self.app.delete('/jugadores/EjemploPost')
        self.assertEqual(respuesta.status_code, 204, "Ha habido algún error en el borrado de EjemploPost.")
        self.assertEqual(respuesta.headers['content-type'], 'application/json', "Tipo MIME de la cabecera no es JSON.")

        respuesta = self.app.get('/jugadores')
        self.assertEqual(respuesta.status_code, 200, "El recurso de jugadores no se encuentra disponible.")
        self.assertEqual(respuesta.headers['content-type'], 'application/json', "Tipo MIME de la cabecera no es JSON.")
        contenido = obtenerContenidoPaquete(respuesta)
        self.assertEqual(len(contenido.keys()), 3, "Número de jugadores debería encontrarse en 3.")

        respuesta = self.app.get('/jugadores/EjemploPost')
        self.assertEqual(respuesta.status_code, 404, "El recurso EjemploPost no debería poder encontrarse.")
        self.assertEqual(respuesta.headers['content-type'], 'application/json', "Tipo MIME de la cabecera no es JSON.")

        respuesta = self.app.delete('/jugadores/jugador76')
        self.assertEqual(respuesta.status_code, 204, "Ha habido algún error en el borrado de una ruta que no existe.")
        self.assertEqual(respuesta.headers['content-type'], 'application/json', "Tipo MIME de la cabecera no es JSON.")

    def test8PutJugador(self):

        respuesta = self.app.put("/jugadores/EjemploPut",data=Jugador("EjemploPut", "Alberto", "Soriano Martinez", 15, ["juego1", "juego2", "juego3"], True).__dict__())
        self.assertEqual(respuesta.status_code, 200, "El recurso no se ha puesto correctamente en el recurso /jugadores/EjemploPut.")
        self.assertEqual(respuesta.headers['content-type'], 'application/json', "Tipo MIME de la cabecera no es JSON.")
        contenido = obtenerContenidoPaquete(respuesta)
        self.assertEqual(contenido['Nick'], "EjemploPut", "Parece que no se ha realizado el put correctamente.")

        respuesta = self.app.get('/jugadores')
        self.assertEqual(respuesta.status_code, 200, "El recurso de jugadores no se encuentra disponible.")
        self.assertEqual(respuesta.headers['content-type'], 'application/json', "Tipo MIME de la cabecera no es JSON.")
        contenido = obtenerContenidoPaquete(respuesta)
        self.assertEqual(len(contenido.keys()), 4, "Debe haber 4 jugadores en este punto.")

        respuesta = self.app.put("/jugadores/Malcaide", data=Jugador("Malcaide", "Alberto", "Soriano Martinez", 15, ["juego1", "juego2", "juego3"], True).__dict__())
        self.assertEqual(respuesta.status_code, 200,"El recurso no se ha puesto correctamente en el recurso /jugadores/Malcaide.")
        self.assertEqual(respuesta.headers['content-type'], 'application/json', "Tipo MIME de la cabecera no es JSON.")
        contenido = obtenerContenidoPaquete(respuesta)
        self.assertEqual(contenido['Nombre'], "Alberto", "Parece que no se ha realizado el put correctamente.")
        self.assertEqual(contenido['Edad'], 15, "Parece que no se ha realizado el put correctamente.")

    def test9DeleteJugadores(self):
        respuesta = self.app.get('/jugadores')
        self.assertEqual(respuesta.status_code, 200, "El recurso de jugadores no se encuentra disponible.")
        self.assertEqual(respuesta.headers['content-type'], 'application/json', "Tipo MIME de la cabecera no es JSON.")
        contenido = obtenerContenidoPaquete(respuesta)
        self.assertGreater(len(contenido.keys()), 0, "Deberíamos tener jugadores disponibles en este punto.")
        respuesta = self.app.delete('/jugadores')
        self.assertEqual(respuesta.status_code, 204, "Ha habido algún error en el borrado de los jugadores")
        self.assertEqual(respuesta.headers['content-type'], 'application/json', "Tipo MIME de la cabecera no es JSON.")


        # Debemos de dejar la base de datos como estaba al principio
        j1 = Jugador("Hapneck", "Alejandro", "Campoy Nieves", 22, ["Fortnite", "Hollow Knight", "The Witcher"], True)
        j2 = Jugador("Malcaide", "Alfonso", "Barragan Lara", 22, ["Counter Strike"], True)
        j3 = Jugador("Rekkles", "Juan", "Martinez Casado", 22, ["Fortnite", "League of Legends", "Counter Strike"],False)
        self.app.put("/jugadores/Hapneck", data=j1.__dict__())
        self.app.put("/jugadores/Malcaide", data=j2.__dict__())
        self.app.put("/jugadores/Rekkles", data=j3.__dict__())


if __name__ == '__main__':
    unittest.main()