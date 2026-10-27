from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, FloatField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class StaffForm(FlaskForm):
    """Staff Management Form (Admin Only)."""
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    designation = StringField('Job Designation', validators=[DataRequired(), Length(min=2, max=50)])
    salary = FloatField('Monthly Salary (₹)', validators=[
        DataRequired(), 
        NumberRange(min=0.0, message="Salary must be a positive number.")
    ])
    address = TextAreaField('Residential Address', validators=[DataRequired()])
    joining_date = DateField('Date of Joining', format='%Y-%m-%d', validators=[DataRequired()])
    photo = FileField('Staff Photograph', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Only image files are allowed!')
    ])
    submit = SubmitField('Save Staff Record')
