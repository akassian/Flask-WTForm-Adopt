from models import db, Pet
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
Pet.query.delete()

# Add pets
bongo = Pet(name="Bongo", species="Orangatang", photo_url="https://thumbs.dreamstime.com/b/hello-orangatang-animal-looking-you-his-pen-was-taken-oz-years-ago-93938588.jpg", age="adult", notes="A wise, kind soul.", available=True)
mayo = Pet(name="Mayo", species="Dog", age="senior", notes="He likes mayonaise.", available=False)

# Add new objects to session, so they'll persist
db.session.add(bongo)
db.session.add(mayo)

# Commit--otherwise, this never gets saved!
db.session.commit()
