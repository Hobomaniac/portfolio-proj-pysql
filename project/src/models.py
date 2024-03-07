from flask_sqlalchemy import SQLAlchemy 
import datetime

db = SQLAlchemy()

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)

    def __init__(self, username:str, password:str, email:str):
        self.username = username
        self.password = password
        self.email = email

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email
        } 

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    birthdate = db.Column(db.Date)

    def __init__(self, first_name:str, last_name:str, birthdate=None):
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthdate": self.birthdate
        }
    
routes_labels_table = db.Table(
    "routes_labels",
    db.Column("route_id", 
              db.Integer, 
              db.ForeignKey("routes.id"), 
              primary_key=True),
    db.Column("label_id", 
              db.Integer, 
              db.ForeignKey("labels.id"), 
              primary_key=True),
)

class Route(db.Model):
    __tablename__ = "routes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    location = db.Column(db.String(128))
    distance = db.Column(db.Numeric)
    time_length = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    labels = db.relationship('Label', secondary=routes_labels_table, backref='routes')

    def __init__(self, name:str, date, location:str, distance:float, time_length:int, user_id:int):
        self.name = name
        self.date = date
        self.location = location
        self.distance = distance
        self.time_length = time_length
        self.user_id = user_id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "location": self.location,
            "distance": self.distance,
            "time_length": self.time_length,
            "user_id": self.user_id
        }

class Label(db.Model):
    __tablename__ = "labels"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name:str):
        self.name = name

    def serialize(self):
        return {
            "id": self.id, 
            "name": self.name
        }

class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    time_stamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    route_id = db.Column(db.Integer, db.ForeignKey("routes.id"), nullable=False)

    def __init__(self, title:str, description:str, time_stamp, route_id:int):
        self.title = title
        self.description = description
        self.time_stamp = time_stamp
        self.route_id = route_id

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "time_stamp": self.time_stamp,
            "route_id": self.route_id 
        }
