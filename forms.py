from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, ValidationError
from wtforms.validators import InputRequired, Optional, Length, URL

class AddPetForm(FlaskForm):
    """Form for adding pets."""
    def validate_pet(form, field):
        pets = ['Cat', 'Dog', 'Porcupine', 'Orangatang']
        if (field.data.title() not in pets):
            raise ValidationError('Pet must be either “Cat”, “Dog”, “Porcupine”, or "Orangatang"')

    def validate_age(form, field):
        ages = ['Baby', 'Young', 'Adult', 'Senior']
        if (field.data.title() not in ages):
            raise ValidationError('Age must be either “Baby”, “Young”, “Adult”, or "Senior"')

    name = StringField("Pet Name", validators=[InputRequired(),Length(max=30)])
    species = StringField("Species", validators=[InputRequired(), Length(max=30), validate_pet])
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    age = SelectField('Age',
    choices=[('baby', 'Baby'), ('young', 'Young'), ('adult', 'Adult'), ('senior', 'Senior')], validators=[InputRequired(), validate_age])
    notes = StringField("Notes", validators=[Optional(), Length(max=400)])

class EditPetForm(FlaskForm):
    """Form for editing pets."""
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    notes = StringField("Notes", validators=[Optional(), Length(max=400)])
    available = BooleanField("Available")
