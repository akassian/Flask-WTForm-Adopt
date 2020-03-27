from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
from petfinder_access import API_KEY, SECRET_KEY
import requests

app = Flask(__name__)

app.config["SECRET_KEY"] = "Shhhhh"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

DEFAULT_PIC = "https://images.pexels.com/photos/356079/pexels-photo-356079.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260"
auth_token = None

@app.before_first_request
def refresh_credentials():
    global auth_token
    auth_token = update_auth_token_string()

def update_auth_token_string():
    resp = requests.post("https://api.petfinder.com/v2/oauth2/token", data={
        "grant_type": "client_credentials",
        "client_id": f"{API_KEY}",
        "client_secret": f"{SECRET_KEY}"
        })
    resp = resp.json()

    return resp.get("access_token", resp)


@app.route("/")
def home():
    """
    GET homepage
    (list of all pets in pets table of adopt db!)
    """

    pets = Pet.query.all()

    resp = requests.get("https://api.petfinder.com/v2/animals", 
                params={"limit":"1", "sort":"random"},
                headers={"Authorization": f"Bearer {auth_token}"})
    
    resp = resp.json()
    resp = resp["animals"][0]
    print("\n\n\n This is your petfinder:", resp, "\n\n\n")
    
    petfinder = {"age":resp["age"], "name":resp["name"], "photo_url":resp["photos"][0]["medium"]}
    
    return render_template("/pets.html", pets=pets, petfinder=petfinder)

@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """
    Pet add form;
    validates and handle adding of new pet into pets table
    Also handles GET of add form
    """

    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data or None
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name = name, species = species, photo_url = photo_url, age = age, notes = notes)

        db.session.add(pet)
        db.session.commit()

        flash(f"Added {name}!")
        return redirect("/")

    else:
        return render_template(
            "add_pet.html", form=form)

@app.route("/<int:id>", methods=["GET", "POST"])
def pet_info(id):
    """
    Pet info and edit form;
    validates and handle editing of pet into pets table
    Also handles GET of pet info / edit form
    """

    pet = Pet.query.get_or_404(id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        photo_url = form.photo_url.data
        photo_url = photo_url if photo_url else DEFAULT_PIC
        notes = form.notes.data
        available = form.available.data

        # TO NOT CHANGE PICTURE WHEN EMPTY STRING!!!
        # if photo_url is not None:
        #     pet.photo_url = photo_url
        pet.photo_url = photo_url
        pet.notes = notes
        pet.available = available

        db.session.commit()

        flash(f"Edited {pet.name}!")
        return redirect(f"/{id}")

    else:
        return render_template(
            "pet_info.html", pet=pet, form=form)