from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired, Optional, Length

class AddPetForm(FlaskForm):
    """Form for adding pets."""

    name = StringField("Pet Name", validators=[InputRequired(),Length(max=30)])
    species = StringField("Species", validators=[InputRequired(), Length(max=30)])
    photo_url = StringField("Photo URL")
    age = SelectField('Age',
    choices=[('baby', 'Baby'), ('young', 'Young'), ('adult', 'Adult'), ('senior', 'Senior')], validators=[InputRequired()])
    notes = StringField("Notes", validators=[Optional(), Length(max=400)])
