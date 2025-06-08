from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    middlename = StringField('Middle Name')
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    contact_number = StringField('Contact Number', validators=[DataRequired()])
    address = StringField('Street Address', validators=[DataRequired()])
    submit = SubmitField('Register')

class TicketForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired()])
    event_id = StringField('Event ID', validators=[DataRequired()])
    number_of_tickets = StringField('Number of Tickets', validators=[DataRequired()])
    tickets_type = StringField('Ticket Type', validators=[DataRequired()])
    submit = SubmitField('Buy Ticket')