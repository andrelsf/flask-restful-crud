from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel


app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)

# Add recursos disponiveis da API
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hotel/<string:hotel_id>')


if __name__ == '__main__':
    app.run(debug=True)
