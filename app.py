"""Flask app for Cupcakes"""
from flask import Flask, render_template, request, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "poiawhefiusiuawe"


@app.route("/", methods=['GET', 'POST'])
def index():
    """ Homepage"""

    return render_template("index.html", cupcakes=Cupcake.query.all())


@app.route("/api/cupcakes")
def get_cupcakes_data():
    """ Get data about all cupcakes.
        Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}.
        The values should come from each cupcake instance. """

    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize_cupcake() for cupcake in cupcakes]
    return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake_details(cupcake_id):
    """ Get data about a single cupcake.
    Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.
    This should raise a 404 if the cupcake cannot be found. """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize_cupcake()
    return jsonify(cupcake=serialized)


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake_details():
    """ Create a cupcake with flavor, size, rating and image data from the 
        body of the request.
        Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}. """

    # import pdb; pdb.set_trace()

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    print("************************************************************")
    db.session.add(new_cupcake)
    db.session.commit()
    
    serialized = new_cupcake.serialize_cupcake()

    return (jsonify(cupcake=serialized), 201)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """ Update cupcake details
    Respond with JSON of the newly-updated cupcake,
    like this: {cupcake: {id, flavor, size, rating, image}}. """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json['flavor']
    cupcake.size = request.json['size']
    cupcake.rating = request.json['rating']
    cupcake.image = request.json['image']

    db.session.commit()

    serialized = cupcake.serialize_cupcake()

    return (jsonify(cupcake=serialized), 200)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """ Delete cupcake with the id passed in the URL.
    Respond with JSON like {message: "Deleted"}. """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return (jsonify(message='Deleted'))
