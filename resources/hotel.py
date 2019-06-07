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
    
    def __init__(self):
        self.mongo = MongoDBHoteis()
        self.mongo = self.mongo.get_connection_hoteis()

    def get_hotel(self, hotel_id):
        collection_hoteis = self.mongo.get_collection(name='hoteis')
        for hotel in collection_hoteis.find({}, {"_id": False}):
            if hotel['hotel_id'] == hotel_id:
                return True
        return False


    def get(self, hotel_id):
        collection_hoteis = self.mongo.get_collection(name='hoteis')
        for hotel in collection_hoteis.find({}, {"_id": False}):
            if hotel['hotel_id'] == hotel_id:
                return hotel, 200
        else:
            return {'message': 'Hotel not found.'}, 404


    def post(self, hotel_id):
        if not hotel_id:
            return {'warnning': 'ERROR'}, 400
        if (self.get_hotel(hotel_id=hotel_id)):
            return {'warnning': 'ID already registered.'}, 409
        args_req = reqparse.RequestParser(bundle_errors=True)
        args_req.add_argument('nome', type=str, required=True)
        args_req.add_argument('estrelas', type=float, required=True)
        args_req.add_argument('diaria', type=float, required=True)
        args_req.add_argument('cidade', type=str, required=True)
        hotel = args_req.parse_args()
        hotel['hotel_id'] = hotel_id
        collection_hoteis = self.mongo.get_collection(name='hoteis')
        try:
            collection_hoteis.insert_one(hotel)
        except TypeError as err:
            return {'error': str(err)}, 500
        else:
            return {'message': 'success', 'status': 201}, 201
        
