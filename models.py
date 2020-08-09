from datetime import datetime
from config import db, ma
from marshmallow_sqlalchemy import ModelSchema

class Restaurant(db.Model):
    __tablename__ = "tb_restaurants"
    id = db.Column(db.String(255), primary_key=True)
    rating = db.Column(db.Integer)
    name = db.Column(db.String(255))
    site= db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    street = db.Column(db.String(255))
    city= db.Column(db.String(255))
    state = db.Column(db.String(255))
    lat= db.Column(db.Float)
    lng= db.Column(db.Float)

class RestaurantSchema(ModelSchema):
    class Meta:
        model = Restaurant 
        sqla_session = db.session