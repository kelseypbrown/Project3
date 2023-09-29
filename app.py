from flask import Flask, render_template
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

# Create an SQLAlchemy engine and session
engine = create_engine("sqlite:///data/spotify2023.db")
Base =automap_base()
Base.prepare(engine,reflect=True)
Table1=Base.classes.table1


# Create the Flask app
app = Flask(__name__)

@app.route('/')
def home():
    session= Session(engine)
    data = session.query(Table1).all()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
