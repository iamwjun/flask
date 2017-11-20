from flask import Flask, request
from flask_restful import Resource, Api
# from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import pymysql
from json import dumps
from flask.ext.jsonpify import jsonpify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] == 'mysql+pymysql://park:park@121.41.51.151:3306/park?charset=utf8'
db = SQLAlchemy(app)

class parking_lot(Resource):
    def get(self):
        query = self.query.all()
        return {'alls': [i[0] for i in query.cursor.fetclall()]}

api.add_resource(AllParkingLot, '/allParkingLot')

if __name__ == '__main__':
    app.run()

