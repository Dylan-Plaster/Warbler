from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')
    header_image_url = StringField('(Optional) Header Image Url')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class UserEditForm(FlaskForm):
    """User edit form"""
    username = StringField('Username', validators=[DataRequired(message="This field is required")])
    email = StringField('Email', validators=[DataRequired(message="This field is required"), Email(message="Email not valid")])
    image_url = StringField('(Optional) Profile Image URL')
    header_image_url = StringField('(Optional) Header Image URL')
    bio = StringField('User Bio (Optional)')
    password = PasswordField('Password')
