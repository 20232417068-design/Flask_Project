from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    description = db.Column(db.Text)
    image = db.Column(db.String(100))
    category = db.Column(db.String(50))   


    category = db.Column(db.String(50))


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    message = db.Column(db.Text)
       
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    address = db.Column(db.Text)
    items = db.Column(db.Text)
    user_id = db.Column(db.Integer)  

    date = db.Column(db.DateTime, default=datetime.utcnow)   
    status = db.Column(db.String(50), default="Pending")     
    is_hidden = db.Column(db.Boolean, default=False)  