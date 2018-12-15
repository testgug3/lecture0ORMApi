import os
from flask import Flask, render_template, request
from models import *

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
    passenger = Passenger(name=name, flight_id=flight_id)
    db.session.add(passenger)
    db.session.commit()
    return render_template("success.html")

@app.route("/flights")
def flights():
    """List all flights."""
    #flights = db.session.query(Flight).all() #working code
    # flights = Flight.query().all() #'BaseQuery' object is not callable
    flights = Flight.query.all()
    return render_template("flights.html", flights=flights)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    """Lists details about a single flight."""

    #Make sure the flight exists.
    #flight = db.session.query(Flight).get(flight_id)
    flight = Flight.query.get(flight_id)
    if flight is None:
        return render_template("error.html",message="No such flights.")
    # # Get all passengers.
    #passengers = db.session.query(Passenger).filter_by(flight_id) not working either
    #passengers = Passenger.query.filter_by(flight_id).all() #not working
    passengers = Passenger.query.filter_by(flight_id=flight_id).all()
    return render_template("flight.html", flight=flight, passengers=passengers)


