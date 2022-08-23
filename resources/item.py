import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

#Esta clase esta en la carpeta resources, 
#ya que unicamente se encarga de interactuar con la API
#OJO : Todos los meatodos devuelven una respuesta JSON

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank!'
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help='Every item needs a store id.'
    )
    
    # Protect a route with jwt_required, which will kick out requests
    # without a valid JWT present.
    @jwt_required() 
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message": "An error occurred getting the item."}, 500

        if item:
            return item.json()
        return {'message':'Item not found'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name): #Se podria poner tambien Item.find_by....
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        
        data = Item.parser.parse_args()
        #Si no tiene una cabecera de tipo content type esto va a petar -> force= true() no se necesita el encabezado content type
        item = ItemModel(name, data['price'], data['store_id']) 
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."},500 #internal server error
        return item.json(), 201
    
    def delete(self, name):
        #global items
        
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()    
        return {'message': 'Item deleted'},200

    def put(self, name):
        #Esto se usa para obligar a que lo que se obtiene del JSON tenga este formato.
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
    
        if item is None:
            try:
                item= ItemModel.find_by_name(name, data['price'], data['store_id']) # Esto se puede simplificar por **data
            except:
                return {"message": "An error occurred inserting the item."},500

        else:
            try:
                item.price = data['price']
            except:
                return {"message": "An error occurred updating the item."},500
        item.save_to_db() 

        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items' : [x.json() for x in ItemModel.query.all()]}