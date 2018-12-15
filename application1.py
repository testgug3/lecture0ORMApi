import os
from flask import Flask, render_template, request
from models1 import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("psql_db_url")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    flights = Flight.query.all()
    return render_template("index.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
    """Book a flight."""

    #Get form information
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Invalid flight number.")
    
    #make sure flight exists
    flight = Flight.query.get(flight_id)
    if flight is None:
        return render_template("error.html", message="No such flight with that id.")
    #Add passenger.
    flight.add_passenger(name)
    return render_template("success.html")

@app.route("/flights")
def flights():
    """List all flights."""
    flights = Flight.query.all()
    return render_template("flights.html", flights=flights)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    """Lists details about a single flight."""

    flight = Flight.query.get(flight_id)
    if flight is None:
        return render_template("error.html",message="No such flights.")
    passengers = flight.passengers
    return render_template("flight.html", flight=flight, passengers=passengers)


