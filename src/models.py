from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = 'people'
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
            "skin_color": self.skin_color,
            "homeworld_id": self.homeworld_id,
            "homeworld_name": self.homeworld.name,
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__ = 'planets'
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
    #residents_id = db.Column(db.Integer, db.ForeignKey('people.id'))
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

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    element_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    #people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable = False)
    #planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable = False)
    user = db.relationship(User)
    #people = db.relationship(People)
    #planet = db.relationship(Planets)

    def __repr__(self):
        return '<Favorite %r>' % self.type % self.element_id

    def serialize(self):
        return {
            "type": self.type,
            "element_id": self.element_id,
            "user_info": self.user.serialize()
            # do not serialize the password, its a security breach
        }
