class Jugador:
    def __init__(self,nick,nombre,apellidos,edad,videojuegos,competitivo):
        self.nick=nick
        self.nombre=nombre
        self.apellidos=apellidos
        self.edad=edad
        self.videojuegos=videojuegos
        self.competitivo=competitivo

    def __dict__(self):
        d = {
            "Nick": self.nick,
            "Nombre": self.nombre,
            "Apellidos": self.apellidos,
            "Edad": self.edad,
            "Videojuegos": self.videojuegos,
            "Competitivo": self.competitivo
        }

        return d

    def setNick(self,nick):
        self.nick=nick

    def aniadirVideojuego(self,juego):
        self.videojuegos.append(juego)

    def eliminarVideojuego(self,juego):
        if(juego in self.videojuegos):
            self.videojuegos.remove(juego)



