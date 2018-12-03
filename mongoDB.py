import pymongo

class BaseDatos:
    def __init__(self,direccion):
        MONGODB_URI = direccion
        client = pymongo.MongoClient(MONGODB_URI, connectTimeoutMS=40000)
        db = client.get_database()
        self.jugadores = db.jugadores


    def getJugador(self,jugador_nick):
        jugador = self.jugadores.find_one({"Nick":jugador_nick})
        del jugador['_id']
        return jugador

    def getJugadores(self):
        salida = {}
        for j in self.jugadores.find():
            del j['_id']
            salida[j['Nick']]=j
        return salida


    def insertJugador(self,jugador):
        entrada = jugador.__dict__()
        if(self.jugadores.find_one({"Nick":entrada['Nick']})):
            return False
        else:
            self.jugadores.insert_one(entrada)
            return True

    def updateJugador(self, jugador_nick, updates):
        try:
            jugador = self.getJugador(jugador_nick)
            self.jugadores.update_one({'Nick': jugador['Nick']}, {'$set': updates}, upsert=False)
        except:
            print("Oops!! Se pretende actualizar una entrada inexistente.")

    def removeJugador(self,jugador_nick):
        self.jugadores.delete_one({"Nick":jugador_nick})

    def mostrarJugadores(self):
        cursor = self.jugadores.find()
        for j in cursor:
            print(j['Nick'], ' - ', j['Nombre'], ' - ', j['Apellidos'], ' - ', j['Edad'], ' - ',
                  j['Videojuegos'], ' - ', j['Competitivo'])

    def removeJugadores(self):
        for j in self.jugadores.find():
            self.removeJugador(j['Nick'])

    def getSize(self):
        return self.jugadores.count_documents({})


