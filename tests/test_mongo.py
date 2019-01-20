import sys
sys.path.append("../")

import unittest
from model import Jugador
from mongoDB import BaseDatos
import pymongo

class TestModel(unittest.TestCase):

    def setUp(self):
        self.mongo = BaseDatos("mongodb://127.0.0.1:27017/MiBaseDatos",True)
        self.mongo.removeJugadores()
        self.prueba = Jugador("Ejemplo", "Alberto", "Soriano Martinez", 150, ["juego1", "juego2", "juego3"], True)

    def test1Tipo(self):
        self.mongo.insertJugador(self.prueba)
        self.assertIsInstance(self.mongo.getJugador("Ejemplo"),dict,"El elemento sacado desde la base de datos no es un diccionario.")
        self.mongo.removeJugador("Ejemplo")

    def test2GetJugador(self):
        diccionario = self.prueba.__dict__()
        self.mongo.insertJugador(self.prueba)
        self.assertEqual(self.mongo.getJugador("Ejemplo"),diccionario,"El jugador de ejemplo no se ha obtenido correctamente de la base de datos.")
        self.mongo.removeJugador("Ejemplo")

    def test3GetJugadoresInsertRemoveAllSize(self):
        prueba2 = Jugador("Ejemplo2", "Alberto", "Soriano Martinez", 150, ["juego1", "juego2", "juego3"], True)
        self.mongo.insertJugador(self.prueba)
        self.mongo.insertJugador(prueba2)
        self.assertEqual(self.mongo.getSize(),2,"El número de documentos dentro de la base de datos debería ser 2 en este punto.")
        salida=self.mongo.getJugadores()
        self.assertEqual(salida["Ejemplo"],self.prueba.__dict__(),"El primer ejemplo no se ha insertado correctamente.")
        self.assertEqual(salida["Ejemplo2"],prueba2.__dict__(),"El segundo ejemplo no se ha insertado correctamente")
        self.mongo.removeJugadores()
        self.assertEqual(self.mongo.getSize(),0,"No se han eliminado correctamente todos los documentos de mongoDB.")

    def test4RemoveJugador(self):
        self.mongo.insertJugador(self.prueba)
        self.assertEqual(self.mongo.getSize(), 1, "El número de documentos dentro de la base de datos debería ser 1 en este punto.")
        self.mongo.removeJugador("Ejemplo")
        self.assertEqual(self.mongo.getSize(), 0, "La base de datos debería de estar vacía en este punto.")

    def test5InsertarDosIguales(self):
        self.mongo.insertJugador(self.prueba)
        self.assertEqual(self.mongo.getSize(), 1, "El número de documentos dentro de la base de datos debería ser 1 en este punto.")
        self.mongo.insertJugador(self.prueba)
        self.assertEqual(self.mongo.getSize(), 1, "El número de documentos dentro de la base de datos debería seguir siendo 1 en este punto.")
        self.mongo.removeJugadores()

    def test6UpdateJugador(self):
        self.mongo.insertJugador(self.prueba)

        updates= {'Nombre':'Acierto'}#,'videojuegos':['prueba1','prueba2']}
        self.mongo.updateJugador("Ejemplo",updates)
        self.assertEqual(self.mongo.getJugador("Ejemplo")['Nombre'],'Acierto',"El Nombre de la entrada de ejemplo no se ha actualizado correctamente")
        self.mongo.removeJugadores()


if __name__ == '__main__':
    unittest.main()
