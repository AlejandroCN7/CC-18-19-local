import unittest
from model import Jugador

class TestModel(unittest.TestCase):

    # Definimos dos jugadores con los que vamos a realizar las pruebas
    def setUp(self):
        self.prueba = Jugador("Ejemplo","Alberto","Soriano Martinez",150,["juego1","juego2","juego3"],True)
        self.prueba2 = Jugador("Ejemplo", "Alberto", "Soriano Martinez", 150, ["juego1", "juego2", "juego3"], True)

    # Comprobamos que la instancia creada es del tipo Jugador
    def testTipoCreacion(self):
        self.assertIsInstance(self.prueba,Jugador,"Tipo de objeto jugador incorrecto.")

    # Comprobamos que dos instancias con los mismos atributos no son la misma (ocupa zonas de memoria distintas)
    def testUnicidad(self):
        self.assertIsNot(self.prueba,self.prueba2,"Dos objetos con los mismos atributos no pueden ser el mismo.")

    # Comprobamos que el cambio de un atributo se realiza correctamente.
    def testCambioNick(self):
        self.prueba.setNick("nuevoNick")
        self.assertIsInstance(self.prueba.nick,str,"El tipo del campo nick no es correcto al cambiarlo")
        self.assertEqual(self.prueba.nick,"nuevoNick","El atrubuto Nick no se ha modificado correctamente.")

    # Comprobamos que se puede añadir un videojuego a la lista de un jugador correctamente.
    def testInsertar(self):
        self.prueba.aniadirVideojuego("Nuevo Juego")
        self.assertIn("Nuevo Juego",self.prueba.videojuegos,"No se ha agregado un videojuego al jugador correctamente.")

    # Del mismo modo, comprobamos que es posible eliminar un videojuego de la lista
    def testEliminar(self):
        self.assertEqual(len(self.prueba.videojuegos),3,"No se ha creado el vector de videojuegos del jugador correctamente.")
        self.prueba.eliminarVideojuego("Juego que no tiene el jugador")
        self.assertEqual(len(self.prueba.videojuegos), 3, "Se eliminan juegos que no existen??")
        self.prueba.eliminarVideojuego("juego2")
        self.assertNotIn("juego2",self.prueba.videojuegos,"Los videojuegos especificados no se eliminan bien del jugador.")

if __name__ == '__main__':
    unittest.main()



