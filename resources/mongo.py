from pymongo import MongoClient

class MongoDBHoteis():
    
    def __init__(self):
        self.client = MongoClient(
                "mongodb+srv://restapiuser:r3sT4p1uS3r9@cluster0-unusf.mongodb.net/test?retryWrites=true&w=majority"
            )

    def get_connection_hoteis(self):
        return self.client.get_database(name='dbhoteis')
