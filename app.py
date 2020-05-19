import sqlalchemy
import sqlite3
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect
from flask import Flask, jsonify
import numpy as np



# Database Setup

conn_str = 'sqlite:///Resources/hawaii.sqlite'
conn = create_engine(conn_str)
inspector = inspect(conn)

#reflect an existing database into a new model
Base = automap_base()

# reflect the tables in database
Base.prepare(conn, reflect=True)

#save references to the table
Measurement = Base.classes.measurement
Station= Base.classes.station


# Flask Setup

app = Flask(__name__)

#Use Flask to create your routes.

@app.route('/')
def home():
    " " "List all availbale api routes" " "
    return (
        "Home Page<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api.v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdate<br/>"
        f"/api/v1.0/enddate<br/>"
    )
#Convert the query results to a dictionary using `date` as the key and `prcp` as the value. 
# Return the JSON representation of your dictionary.

@app.route('/api/v1.0/precipitation')
def precipitation():
    session= Session(conn)
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    data =[]

    for date, prcp in results:
        measurement_dict ={}
        measurement_dict["date"]= date
        measurement_dict["prcp"]= prcp
        data.append(measurement_dict)
    return jsonify(data)
    session.close()

#Returning a JSON list of temperature observations (TOBS) for the previous year")
@app.route('/api/v1.0/tobs')
def tobs():
    session= Session(conn)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>'2015-12-31').\
        filter(Measurement.date <'2017-01-01')
    
    tobsdata =[]

    for date, tobs in results:
        tobs_dict ={}
        tobs_dict["date"]= date
        tobs_dict["tobs"]= tobs
        tobsdata.append(tobs_dict)
    return jsonify(tobsdata)
    session.close()
    
#Return a JSON list of stations from the dataset.  
@app.route('/api/v1.0/station')
def station():
    session= Session(conn)
    names = session.query(Station.id, Station.name).all()
    all_stations = list(np.ravel(names))

    return jsonify(all_stations)

  
if __name__== "__main__":
        app.run(debug=True)
