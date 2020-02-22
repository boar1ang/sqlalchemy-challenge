#sqlalchemy-challenge homework
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import join
import json
import numpy as np
import warnings
warnings.filterwarnings('ignore')

engine = create_engine("sqlite:///data/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station

# #Create Flask app:
app = Flask(__name__)
@app.route("/")
def home():
    print("Server received request for Climate App 'Home' page.")
    return("Welcome to the Climate App Home page!<br/>"
           "This site provides access to an amazing collection of climate data from Hawaii.<br/>"
           "Would you like to use our API? Available API routes include:<br/>"
           f"Precipitation: /api/v1.0/precipitation<br/>"
           f"Weather stations: /api/v1.0/stations<br/>"
           f"Temperature observations over 1 year: /api/v1.0/tobs<br/>" 
           f"Temperature observations from start date: /api/v1.0/tobs<br/>"
           f"Temperature from specified start date to specified end date: /api/v1.0/<start> and /api/v1.0/<start>/<end><br/>")

#### API route 1/5:
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    sel = [Measurement.prcp, Measurement.date]
    result=session.query(*sel).all()
    session.close()
    
    precipitation = []
    for date, prcp in result:
        prcp_dict={}
        prcp_dict["precipitation"] = prcp
        prcp_dict["date"] = date
        precipitation.append(prcp_dict)
        
    precipitation = list(np.ravel(result))    
    return jsonify(precipitation)


    
#### API route 2/5:   
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    sel = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
    result = session.query(*sel).all()  
    session.close()
    
    stations = []
    for station, name, latitude, longitude, elevation in  result:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        stations.append(station_dict)
    stations = list(np.ravel(result))
    return jsonify(stations)


#### API route 3/5:
@app.route("/api/v1.0/tobs")
def temp_obs():
    session = Session(engine)
    latest_obs = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date = dt.datetime.strftime(latest_obs, '%Y-%m-%d') - dt.timedelta(days=365)
    sel = [Measurement.date, Measurement.tobs]
    result = session.query(*sel).all()
    session.close()
     
    temp_obs = []
    for date, tobs in result:
        temp_obs_dict = {}
        temp_obs_dict["date"] = date
        temp_obs_dict["Measurement.tobs"] = tobs
        temp_obs.append(temp_obs_dict)
    temp_obs = list(np.ravel(result))
    return jsonify(temp_obs)
        
#### API route 4/5:    
@app.route("/api/v1.0/<start>")
def temps_from_start(start):
    session = Session(engine)
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >=       start).all()
    session.close()
    
    temps_from_start = []
    for min, avg, max in result:
        temps_from_start_dict = {}
        temps_from_start["min"] = min
        temps_from_start["avg"] = avg
        temps_from_start["max"] = max
        temps_from_start.append(temps_from_start_dict)        
    temps_from_start = list(np.ravel(result))
    return jsonify(temps_from_start)

#### API route 5/5:
@app.route("/api/v1.0/<start>/<end>")
def temps_start_to_end(start, end):
    session = Session(engine)
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >=       start).filter(Measurement.date <= end).all()     
    session.close()
    
    temps_start_to_end = []
    for min, avg, max in result:
        temps_start_to_end_dict = {}
        temps_start_to_end["min"] = min
        temps_start_to_end["avg"] = avg
        temps_start_to_end["max"] = max
        temps_start_to_end.append(temps_start_to_end_dict)
    temps_start_to_end = list(np.ravel(result))
    return jsonify(temps_start_to_end)
           
           
if __name__ == "__main__":
    app.run(debug=True)