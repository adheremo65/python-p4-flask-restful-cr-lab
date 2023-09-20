#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        all_plants = Plant.query.all()
        plants_dict = [item.to_dict() for item in all_plants]
        response = make_response(plants_dict,200)
        return response
    def post(self):
        data = request.get_json()
        request_body = Plant(
            name = data.get("name"),
            image = data.get("image"),
            price = data.get("price"),
        )
        db.session.add(request_body)
        db.session.commit()
        response_dict = request_body.to_dict()
        response = make_response(response_dict,200)
        return response
    
api.add_resource(Plants,"/plants")

class PlantByID(Resource):
    def get(self, id):  # Use the GET method to retrieve a plant by ID
        single_plant = Plant.query.filter_by(id=id).first()
        if single_plant:
            single_dict = single_plant.to_dict()
            response = make_response(single_dict, 200)
            return response
        else:
            return {"error": "Plant not found"}, 404

api.add_resource(PlantByID, "/plants/<int:id>")

    
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
