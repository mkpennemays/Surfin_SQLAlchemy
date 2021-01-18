import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"api/v1.0/tobs"
        f"api/v1.0/<start>"
        f"api/v1.0/<start/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list precipitation for the last year"""
    # Query all passengers
    results = session.query(Measurement.station,Meaurement.date, Measurement.prcp).all()
    #WHERE DATE > ????
    session.close()

    # Convert list of tuples into normal list
    all_precip = list(np.ravel(results))

    return jsonify(all_precip)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all stations
    results = session.query(Station.name).all()

    session.close()

    #use forloop because of amount of data
    #all_stations = list(np.ravel(results))

    return jsonify(all_stations)


if __name__ == '__main__':
    app.run(debug=True)
