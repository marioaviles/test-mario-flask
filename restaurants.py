from flask import make_response, abort
from config import db
from models import Restaurant, RestaurantSchema
import uuid 

def read_all():
    """
    :returns:        json string of list of restaurants
    """
    restaurants = Restaurant.query.order_by(Restaurant.name).all()

    _schema = RestaurantSchema(many=True)
    data = _schema.dump(restaurants)
    return data


def read_one(restaurant_id):
    """
    :param restaurant_id(string):   Id of restaurant
    :return:            restaurant matching object
    """
    restaurant = Restaurant.query.filter(Restaurant.id == restaurant_id).one_or_none()

    if restaurant is not None:

        _schema = RestaurantSchema()
        data = _schema.dump(restaurant)
        return data
    else:
        abort(
            404,
            "Restaurant not found for Id: {_id}".format(_id=_id),
        )


def create(restaurant):
    """
    :param restaurant(object):  restaurant object to create
    :return:       created structure
    """

    # Create a restaurant instance 
    schema = RestaurantSchema()
    new_restaurant = schema.load(restaurant, session=db.session)
    new_restaurant.data['id'] = str(uuid.uuid1())

    obj = Restaurant(**new_restaurant.data)
    # Add the restaurant to the database
    db.session.add(obj)
    db.session.commit()
    # Serialize 
    data = schema.dump(new_restaurant.data)
    return data, 201




def update(restaurant_id, restaurant):
    """
    :param restaurant_id(string):   Id of the restaurant to update
    :param restaurant(object):      restaurant object  in body of request
    :return:            updated restaurant structure
    """

    update_restaurant = Restaurant.query.filter(
        Restaurant.id == restaurant_id
    ).one_or_none()

    # turn the passed in restaurant into a db object
    schema = RestaurantSchema()
    update = schema.load(restaurant, session=db.session)

    # update the object
    db.session.merge(update.data)
    db.session.commit()

    # return updated  structure
    data = schema.dump(update.data)
    return data, 200


def delete(restaurant_id):
    """
    Deletes the indicate restaurant structure
    :param person_id(string):   Id of the restaurant to delete
    :return:            200 on successful delete or 404 if not found
    """
    # Get the restaurant 
    restaurant = Restaurant.query.filter(Restaurant.id == restaurant_id).one_or_none()

    #delete if found
    if restaurant is not None:
        db.session.delete(restaurant)
        db.session.commit()
        return make_response(
            "Restaurant {_id} deleted".format(_id=restaurant_id), 200
        )
    else:
        abort(
            404,
            "Restaurant not found for Id: {_id}".format(id=restaurant_id),
        )

def find_restaurants(longitude, latitude, radius):
    """
    Returns the stats of the nearest restaurant given the distance params
    :param longitude(float):  longitude of starting point
    :param latitude(float):   latitude of starting point
    :param radius(float):   farthest acceptable distance for a restaurant 
    :return:            stats 
    """
    result = db.engine.execute("""select count(*)as count,coalesce (avg(rating),0) as avg, coalesce(stddev(rating),0) as std from tb_restaurants tr  
WHERE ST_DWithin(geom, ST_MakePoint({0},{1})::geography, {2});
""".format(longitude,latitude,radius))
    for row in result:
        return dict(row),200
