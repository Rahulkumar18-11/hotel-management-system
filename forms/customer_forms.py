from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class CustomerForm(FlaskForm):
    """Customer Registration and Editing Form."""
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    address = TextAreaField('Residential Address', validators=[DataRequired()])
    id_type = SelectField('ID Proof Type', choices=[
        ('Aadhaar Card', 'Aadhaar Card'),
        ('Passport', 'Passport'),
        ('Driving License', 'Driving License'),
        ('Voter ID', 'Voter ID'),
        ('Government Issued ID', 'Government Issued ID')
    ], validators=[DataRequired()])
    id_number = StringField('ID Number / Document No.', validators=[DataRequired(), Length(min=4, max=50)])
    id_proof = FileField('Upload ID Proof Document/Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'pdf'], 'Only image files or PDFs are allowed!')
    ])
    submit = SubmitField('Save Customer Details')
