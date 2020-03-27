from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet

app = Flask(__name__)

app.config["SECRET_KEY"] = "Shhhhh"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route("/")
def home():
    "DOCSTRING"

    pets = Pet.query.all()

    return render_template("/pets.html", pets=pets)