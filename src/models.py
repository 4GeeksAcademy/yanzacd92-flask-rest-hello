from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    birth_year = db.Column(db.String(50))
    eye_color = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    hair_color = db.Column(db.String(50))
    height = db.Column(db.Float)
    homeworld_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    mass = db.Column(db.Float)
    name = db.Column(db.String(250), nullable=False)
    skin_color = db.Column(db.String(50))
    created = db.Column(db.DateTime)
    edited = db.Column(db.DateTime)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "name": self.name,
            "skin_color": self.skin_color
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    diameter = db.Column(db.Float)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    gravity = db.Column(db.Float)
    population = db.Column(db.Integer)
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    surface_water = db.Column(db.Integer)
    residents_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    url = db.Column(db.String(250))
    created = db.Column(db.DateTime)
    edited = db.Column(db.DateTime)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water
            # do not serialize the password, its a security breach
        }