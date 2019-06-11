from flask_restful import Resource, reqparse
from resources.mongo import MongoDBHoteis
import json

class Hoteis(Resource):

    def __init__(self):
        self.mongo = MongoDBHoteis()
        self.mongo = self.mongo.get_connection_hoteis()

    def get(self):
        hoteis = list()
        #collection_hoteis = self.dbhoteis.get_collection(name='hoteis')
        collection_hoteis = self.mongo.get_collection(name='hoteis')
        for hotel in collection_hoteis.find({}, {"_id": False}):
            hoteis.append(hotel)
        return { 'hoteis': hoteis }, 200


class Hotel(Resource):
    
    args_req = reqparse.RequestParser(bundle_errors=True)
    args_req.add_argument('nome', type=str, required=True)
    args_req.add_argument('estrelas', type=float, required=True)
    args_req.add_argument('diaria', type=float, required=True)
    args_req.add_argument('cidade', type=str, required=True)


    def __init__(self):
        self.mongo = MongoDBHoteis()
        self.mongo = self.mongo.get_connection_hoteis()
        self._collection_hoteis = self.mongo.get_collection(name='hoteis')


    def get_hotel(self, hotel_id):
        #self._collection_hoteis = self.mongo.get_collection(name='hoteis')
        for hotel in self._collection_hoteis.find({}, {"_id": False}):
            if hotel['hotel_id'] == hotel_id:
                return True
        return False


    def get(self, hotel_id):
        #collection_hoteis = self.mongo.get_collection(name='hoteis')
        for hotel in self._collection_hoteis.find({}, {"_id": False}):
            if hotel['hotel_id'] == hotel_id:
                return hotel, 200
        else:
            return {'message': 'Hotel not found.'}, 404


    def post(self, hotel_id):
        if not hotel_id:
            return {'warnning': 'ERROR'}, 400
        if (self.get_hotel(hotel_id=hotel_id)):
            return {'warnning': 'ID already registred.'}, 409
        hotel = Hotel.args_req.parse_args()
        hotel['hotel_id'] = hotel_id
        try:
            #collection_hoteis = self.mongo.get_collection(name='hoteis')
            self._collection_hoteis.insert_one(hotel)
        except TypeError as err:
            return {'error': str(err)}, 500
        else:
            return {'message': 'success', 'status': 201}, 201
        

    def put(self, hotel_id):
        if not hotel_id:
            return {'warnning': 'ERROR'}, 400
        hotel = Hotel.args_req.parse_args()
        hotel['hotel_id'] = hotel_id
        try:
            #collection_hoteis = self.mongo.get_collection(name='hoteis')
            if (self.get_hotel(hotel_id=hotel_id)):
                self._collection_hoteis.update_one(filter={ 'hotel_id': hotel_id }, update={ "$set": hotel })
                return { 'new_hotel': hotel }, 200
            self._collection_hoteis.insert_one(hotel)
            return { 'new_hotel': hotel }, 201
        except TypeError as err:
            return {'error': str(err)}, 500

    def delete(self, hotel_id):
        if not hotel_id:
            return {'warnning': 'ERROR'}, 400
        try:
            if (self.get_hotel(hotel_id=hotel_id)):
                self._collection_hoteis.delete_one({'hotel_id': hotel_id})
                return { 'message': 'ID deletado[{}]'.format(hotel_id) }, 200
            return { 'message': 'ID not found.' }, 400
        except TypeError as err:
            return { 'error': str(err) }, 500