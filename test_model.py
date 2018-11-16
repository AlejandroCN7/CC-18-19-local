import unittest
from model import Jugador

class TestModel(unittest.TestCase):

    def setUp(self):
        self.prueba = Jugador("Ejemplo","Alberto","Soriano Martinez",150,["juego1","juego2","juego3"],True)
        self.prueba2 = Jugador("Ejemplo", "Alberto", "Soriano Martinez", 150, ["juego1", "juego2", "juego3"], True)

    def testTipoCreacion(self):
        self.assertIsInstance(self.prueba,Jugador,"Tipo de objeto jugador incorrecto.")

    def testUnicidad(self):
        self.assertIsNot(self.prueba,self.prueba2,"Dos objetos con los mismos atributos no pueden ser el mismo.")

    def testCambioNick(self):
        self.prueba.setNick("nuevoNick")
        self.assertIsInstance(self.prueba.nick,str,"El tipo del campo nick no es correcto al cambiarlo")
        self.assertEqual(self.prueba.nick,"nuevoNick","El atrubuto Nick no se ha modificado correctamente.")

    def testInsertar(self):
        self.prueba.aniadirVideojuego("Nuevo Juego")
        self.assertIn("Nuevo Juego",self.prueba.videojuegos,"No se ha agregado un videojuego al jugador correctamente.")

    def testEliminar(self):
        self.assertEqual(len(self.prueba.videojuegos),3,"No se ha creado el vector de videojuegos del jugador correctamente.")
        self.prueba.eliminarVideojuego("Juego que no tiene el jugador")
        self.assertEqual(len(self.prueba.videojuegos), 3, "Se eliminan juegos que no existen??")
        self.prueba.eliminarVideojuego("juego2")
        self.assertNotIn("juego2",self.prueba.videojuegos,"Los videojuegos especificados no se eliminan bien del jugador.")

if __name__ == '__main__':
    unittest.main()



