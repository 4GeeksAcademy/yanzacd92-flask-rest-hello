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
from models import db, User, Favorite
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
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

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

@app.route('/user/<int:user_id>', methods=['GET'])
def user_get(user_id):
    user = User.query.get(user_id)
    if(user is None):
        return jsonify({
            "msg": "User not found"
        }), 404
    return jsonify(user.serialize())

@app.route('/favorite/<element>/<int:element_id>', methods=['POST'])
def favorite_create(element, element_id):
    user_id = request.get_json()["userId"]
    new_favorite = Favorite(type=element, element_id=element_id, user_id=user_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite created"}), 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
