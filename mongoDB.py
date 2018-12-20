import pymongo
import logging

class BaseDatos:
    def __init__(self,direccion,prueba=False):
        logging.info("MONGO:Tratando de conectar con la base de datos.")
        MONGODB_URI = direccion
        client = pymongo.MongoClient(MONGODB_URI, connectTimeoutMS=40000)
        db = client.get_database()
        if (prueba):
            self.jugadores = db.jugadores
        else:
            self.jugadores = db.prueba
        logging.info("MONGO:Conexión completada con éxito.")

    def getJugador(self,jugador_nick):
        jugador = self.jugadores.find_one({"Nick":jugador_nick})
        del jugador['_id']
        logging.info("MONGO:Jugador %s devuelto por la base de datos.",jugador_nick)
        return jugador

    def getJugadores(self):
        salida = {}
        for j in self.jugadores.find():
            del j['_id']
            salida[j['Nick']]=j
        logging.info("MONGO:Todos los jugadores de la base de datos devueltos.")
        return salida


    def insertJugador(self,jugador):
        entrada = jugador.__dict__()
        if(self.jugadores.find_one({"Nick":entrada['Nick']})):
            logging.warning("MONGO:Jugador %s ya existente, no se ha podido insertar en la base de datos.",entrada['Nick'])
            return False
        else:
            self.jugadores.insert_one(entrada)
            logging.info("MONGO:Jugador %s insertado correctamente en la base de datos.", entrada['Nick'])
            return True

    def updateJugador(self, jugador_nick, updates):
        try:
            jugador = self.getJugador(jugador_nick)
            self.jugadores.update_one({'Nick': jugador['Nick']}, {'$set': updates}, upsert=False)
        except:
            print("hola")
            logging.warning("MONGO:Oops!! Se pretende actualizar una entrada inexistente.")

    def removeJugador(self,jugador_nick):
        logging.info("MONGO:Jugador %s eliminado de la base de datos.", jugador_nick)
        self.jugadores.delete_one({"Nick":jugador_nick})

    def mostrarJugadores(self):
        cursor = self.jugadores.find()
        for j in cursor:
            print(j['Nick'], ' - ', j['Nombre'], ' - ', j['Apellidos'], ' - ', j['Edad'], ' - ',
                  j['Videojuegos'], ' - ', j['Competitivo'])

    def removeJugadores(self):
        for j in self.jugadores.find():
            self.removeJugador(j['Nick'])
        logging.info("MONGO:Base de datos vaciada por completo.")

    def getSize(self):
        return self.jugadores.count_documents({})


