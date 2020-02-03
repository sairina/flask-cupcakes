"""Flask app for Cupcakes"""
from flask import Flask, redirect, render_template, request, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "poiawhefiusiuawe"


def serialize_cupcake(cupcake):
    """ Serialize a cupcake SQLAlchemy obj to dictionary """

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }


@app.route("/api/cupcakes")
def get_cupcakes_data():
    """ Get data about all cupcakes.
        Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}.
        The values should come from each cupcake instance. """

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(cupcake) for cupcake in cupcakes]
    return jsonify(cupcakes=serialized)
