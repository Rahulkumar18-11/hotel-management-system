from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from models.user_model import User

class LoginForm(FlaskForm):
    """User Login Form supporting Email, Username, or Phone Number."""
    email = StringField('Username / Email / Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    """User Registration Form for Staff accounts."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number (Optional)', validators=[Optional(), Length(min=10, max=15)])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=6, message="Password must be at least 6 characters long.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])
    role = SelectField('System Role', choices=[
        ('receptionist', 'Receptionist (Front Desk)'),
        ('manager', 'Hotel Manager'),
        ('admin', 'System Administrator')
    ], validators=[DataRequired()])
    submit = SubmitField('Create User Account')

    def validate_username(self, field):
        if User.find_by_username(field.data):
            raise ValidationError('Username is already taken. Please choose another.')

    def validate_email(self, field):
        if User.find_by_email(field.data):
            raise ValidationError('Email address is already registered.')

    def validate_phone(self, field):
        if field.data and User.find_by_phone(field.data):
            raise ValidationError('Phone number is already registered to another user account.')
