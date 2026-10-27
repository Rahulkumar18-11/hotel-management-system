from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, FloatField, IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class RoomForm(FlaskForm):
    """Room Inventory Form."""
    room_number = StringField('Room Number', validators=[DataRequired(), Length(min=1, max=10)])
    room_type = SelectField('Room Category', choices=[
        ('Single', 'Single Room'),
        ('Double', 'Double Room'),
        ('Deluxe', 'Deluxe Suite'),
        ('Suite', 'Executive Suite')
    ], validators=[DataRequired()])
    price_per_day = FloatField('Price per Day (₹)', validators=[
        DataRequired(), 
        NumberRange(min=100.0, message="Price per day must be at least ₹100.")
    ])
    capacity = IntegerField('Capacity (Persons)', validators=[
        DataRequired(), 
        NumberRange(min=1, max=10, message="Capacity must be between 1 and 10.")
    ])
    status = SelectField('Current Status', choices=[
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('maintenance', 'Under Maintenance')
    ], default='available')
    description = TextAreaField('Room Description & Amenities', validators=[Length(max=500)])
    image = FileField('Room Photograph', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Only image files (JPG, PNG, WEBP) are allowed!')
    ])
    submit = SubmitField('Save Room Inventory')
