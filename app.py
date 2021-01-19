import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify

import datetime as dt
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
#lets test

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"api/v1.0/tobs<br/>"
        f"api/v1.0/START-DATE<br/>"
        f"api/v1.0/START-DATE/END-DATE<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list precipitation for the last year in the database"""

    #get last date
    results = session.query(Measurement.date)\
        .order_by(Measurement.date.desc()) 
   
    # Query precipitation data
    results = session.query(Measurement.date,Measurement.prcp)\
        .filter(Measurement.date > '2016-08-23')\
        .order_by(Measurement.date)
    session.close()
    all_precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp

        all_precip.append(precip_dict)
    return jsonify(all_precip)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list tobs for most active station"""

   
    # Query precipititation data
    results = session.query(Measurement.date,Measurement.prcp,Measurement.station)\
        .filter(Measurement.date > '2016-08-23')\
        .filter(Measurement.station == 'USC00519281')\
        .order_by(Measurement.date)
    session.close()

    USC00519281_tobs = []
    for date, tobs, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_dict["tobs"] = tobs

        USC00519281_tobs.append(precip_dict)
    return jsonify(USC00519281_tobs)

@app.route("/api/v1.0/stats/<startDate>")
def stats(startDate):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a min,max,avg"""
    obs_stats = session.query(func.min(Measurement.tobs),\
        func.avg(Measurement.tobs),\
        func.max(Measurement.tobs)).filter(Measurement.date >= startDate).all()
    
    session.close()
    #return jsonify(obs_stats) 
    return(
        f"Stats after {startDate}<br/>"
        f"Minimum Temp: {obs_stats[0][0]}<br/>"
        f"Average Temp: {obs_stats[0][1]}<br/>"
        f"Maximum Temp: {obs_stats[0][2]}<br/>"
    )

@app.route("/api/v1.0/stats/<startDate>/<endDate>")
def stats2(startDate,endDate):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a min,max,avg"""
    obs_stats = session.query(func.min(Measurement.tobs),\
        func.avg(Measurement.tobs),\
        func.max(Measurement.tobs))\
        .filter(Measurement.date >= startDate)\
        .filter(Measurement.date <= endDate).all()
    
    session.close()
    #return jsonify(obs_stats) 
    return(
        f"Stats between {startDate} and {endDate}<br/>"
        f"Minimum Temp: {obs_stats[0][0]}<br/>"
        f"Average Temp: {obs_stats[0][1]}<br/>"
        f"Maximum Temp: {obs_stats[0][2]}<br/>"
    )


 

@app.route("/api/v1.0/stations")
def stations():    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all stations
    results = session.query(Station.name).all()

    session.close()

    all_stations = list(np.ravel(results))
    return jsonify(all_stations)


if __name__ == '__main__':
    app.run(debug=True)
