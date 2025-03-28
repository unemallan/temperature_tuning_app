#!/usr/bin/env python3

import requests
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Weather.sqlite3'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

'''
Define the database model
that is used to store 
the temperature.
'''

class Weather(db.Model):
    datetime = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow())
    temperature = db.Column(db.Integer, nullable=False)
    
'''
Helper function to get temperature
using API
'''

def get_temperature():
    response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    if (
      response.status_code != 204 and
      response.headers["content-type"].strip().startswith("application/json")
    ):
      try:
        #print (response.json())
        return response.json()["current"]["temperature_2m"]
      except ValueError:
        return None


@app.route("/")
def index():
   db.create_all()
   current_temperature = get_temperature()
   new_entry = Weather(temperature=current_temperature)
   db.session.add(new_entry)
   db.session.commit()
   return render_template('index.html')
  
if __name__ == '__main__':
   app.run(debug=True)

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    current_temperature = Weather.query.first()
    return "You entered: " + input_text + "current temperature is:" + str(current_temperature.temperature)

