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

   # Create a horizontal bar chart with track names displayed vertically
    plt.figure(figsize=(10, 6))
    plt.barh(track_names, streams)  # Use plt.barh() for horizontal bars
    plt.xlabel("Streams")
    plt.ylabel("Track Name")  # Adjust the label to indicate track names
    plt.title("Top 10 Songs on Spotify")

    # Rotate the track names vertically
    #plt.gca().invert_yaxis()

    # Convert the chart to a base64-encoded image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()

    session.close()

    # Render the HTML template and pass the base64 image data
    return render_template("index.html", img_base64=img_base64)

if __name__ == "__main__":
    app.run(debug=True)