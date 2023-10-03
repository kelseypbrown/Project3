from flask import Flask, render_template,jsonify 
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Create an SQLAlchemy engine and session
engine = create_engine("sqlite:///data/top2023_genres.db")
Base =automap_base()
Base.prepare(engine,reflect=True)
Table1=Base.classes.table1

#---------------------------------------------------------------------------------------
# Create the Flask app
app = Flask(__name__)

@app.route('/')
def home():
    session = Session(engine)

    # Query the top 10 tracks by streams
    top_tracks = session.query(Table1.track_name, Table1.streams) \
                        .order_by(Table1.streams.desc()) \
                        .limit(10) \
                        .all()

    # Extract the data for the graph
    track_names = [row[0] for row in top_tracks]
    streams = [row[1] for row in top_tracks]

    # Convert the data to a format suitable for Chart.js
    data = {
    "labels": track_names,
    "datasets": [
        {
            "label": 'Streams',
            "data": streams,
            "backgroundColor": 'rgba(0, 128, 0, 0.5)', 
            "borderColor": 'rgba(0, 0, 0, 1)', 
            "borderWidth": 2,
        },
    ],
};

    session.close()

    # Render the HTML template and pass the data for Chart.js
    return render_template("index.html", chart_data=data)

@app.route('/api/music')
def music():
    session = Session(engine)
    # Query the top 10 tracks by streams
    top_tracks = session.query(Table1.track_name, Table1.streams) \
                        .order_by(Table1.streams.desc()) \
                        .all()
    results = [list(t) for t in top_tracks]
    table_results = {
        "table": results
    }
    session.close()
    return jsonify(table_results)

@app.route("/data")
def data():

    return render_template("/data.html")




if __name__ == '__main__':
    app.run(debug=True)