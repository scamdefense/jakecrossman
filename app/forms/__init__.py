from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    """Contact form for booking inquiries."""

    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    production = StringField("Production/Project")
    role = StringField("Role/Opportunity")
    timeline = StringField("Timeline")
    message = TextAreaField("Message", validators=[DataRequired()])
