"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorite, People, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def users_get():
    user = User.query.all()
    user = list(map(lambda u : u.serialize(), user))
    return jsonify(user)

@app.route('/people', methods=['GET'])
def people_get():
    people = People.query.all()
    people = list(map(lambda p : p.serialize(), people))
    return jsonify(people)

@app.route('/planets', methods=['GET'])
def planets_get():
    planets = Planets.query.all()
    planets = list(map(lambda p : p.serialize(), planets))
    return jsonify(planets)

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def user_favorites_get(user_id):
    favorite_query = Favorite.query.filter_by(user_id = user_id)
    favorite_list = list(lambda fav : fav.serialize(), favorite_query)
    return jsonify(favorite_list)

@app.route('/user/<int:user_id>', methods=['GET'])
def user_get(user_id):
    user = User.query.get(user_id)
    if(user is None):
        return jsonify({
            "msg": "User not found"
        }), 404
    return jsonify(user.serialize())

@app.route('/people/<int:people_id>', methods=['GET'])
def person_get(people_id):
    person = People.query.get(people_id)
    if(person is None):
        return jsonify({
            "msg": "Person not found"
        }), 404
    return jsonify(person.serialize())

@app.route('/planets/<int:planet_id>', methods=['GET'])
def planet_get(planet_id):
    planet = Planets.query.get(planet_id)
    if(planet is None):
        return jsonify({
            "msg": "Planet not found"
        }), 404
    return jsonify(planet.serialize())


@app.route('/user', methods=['POST'])
def user_create():
    data = request.get_json()
    new_user = User.query.filter_by(email=data["email"]).first()
    if(new_user is not None):
        return jsonify({
            "msg": "Email registrado"
        }), 400
    new_user = User(email=data["email"], password=data["password"], is_active=True)
    db.session.add(new_user)
    db.session.commit()
    return "ok"

@app.route('/favorite/<string:element>/<int:element_id>', methods=['POST'])
def favorite_create(element, element_id):
    user_id = request.get_json()["userId"]
    new_favorite = Favorite(type=element, element_id=element_id, user_id=user_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite created"}), 201

@app.route('/favorite/>string:element>/<int:element_id>', methods=['DELETE'])
def favorite_planet_delete(element, element_id):
    user_id = request.get_json()["userId"]
    favorite = Favorite.query.filter_by(type=element, element_id=element_id, user_id=user_id).first()
    if(favorite is None):
        return jsonify({"msg": "favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
