import sqlite3
from db import db

# segun el del curso esta clase es una API , no una api rest
# y los dos metodos de abajo son interfaces para nuestro programa

class UserModel(db.Model): # Esto es como decirle que la base de datos va a guardar esste tipo de objetos (Mapeo o asignacion objeto-relacional)
    __tablename__ = 'users' #Esto crea la tabla usuarios
    
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80)) #Limita el tamanio maximo del nombre de usuario
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    #In Python, the @classmethod decorator is used to 
    #declare a method in the class as a class method that can be
    #called using ClassName. MethodName()
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id)