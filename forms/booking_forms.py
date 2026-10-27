from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, FloatField, SubmitField
from wtforms.validators import DataRequired

class BookingForm(FlaskForm):
    """Room Reservation Form."""
    customer_id = SelectField('Select Guest / Customer', validators=[DataRequired()])
    room_id = SelectField('Select Available Room', validators=[DataRequired()])
    check_in = DateField('Check-in Date', format='%Y-%m-%d', validators=[DataRequired()])
    check_out = DateField('Check-out Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Create Booking Reservation')

class CheckoutForm(FlaskForm):
    """Check-out and Final Billing Form."""
    food_charges = FloatField('Additional Food / Room Service Charges (₹)', default=0.0)
    submit = SubmitField('Confirm Check-Out & Generate Invoice')
