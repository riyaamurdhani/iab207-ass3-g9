"""Routes for the application using Blueprint."""
from flask import render_template, redirect, url_for, Blueprint, flash, session
from flask_login import login_required
from app.forms.forms import RegistrationForm, TicketForm
from app.models.user import User
from app.models.event import Event
from app.models.comment import Comment
from app.models.ticket import Ticket
from app import db, bcrypt
import random
import string

index_bp = Blueprint('index', __name__, template_folder='templates')

@index_bp.route('/')
def index():
    session.clear()
    flash('Logged out successfully!', 'success')
    return render_template('index.html')

@index_bp.route('/trigger500')
def trigger_error():
    return 1 / 0  # Division by zero → 500 error

@index_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@index_bp.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@index_bp.route('/home')
def home_page():
    return render_template('home-page.html')

@index_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user:
            error = "User not found!"
        elif not check_password_hash(user.password, password):
            error = "Incorrect password!"
        else:
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index.home_page'))

    return render_template('login.html', error=error)

@index_bp.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Generate random password
        raw_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        hashed_password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

        user = User(
            firstname=form.firstname.data,
            middlename=form.middlename.data,
            lastname=form.lastname.data,
            username=form.username.data,  # assuming it's auto-filled or hidden
            email=form.email.data,
            password=hashed_password,
            contact_number=form.contact_number.data,
            address=form.address.data
        )

        db.session.add(user)
        db.session.commit()

        # Send email with credentials
        msg = Message(
            subject='Your Account Credentials',
            sender='noreply@example.com',
            recipients=[form.email.data]
        )
        msg.body = (
            f"Hello {form.firstname.data},\n\n"
            f"Your login credentials are:\n"
            f"Username: {form.username.data}\n"
            f"Password: {raw_password}\n\n"
            "Please log in and change your password after logging in."
        )
        mail.send(msg)

        flash('Registration successful! Login credentials sent to your email.', 'success')
        return redirect(url_for('auth.login'))

    # Auto-generate a username for display if needed
    generated_username = 'user' + ''.join(random.choices(string.digits, k=5))
    form.username.data = generated_username

    return render_template('registration.html', form=form, generated_username=generated_username)

@index_bp.route('/about-us')
def about_us():
    return render_template('about-us.html')

@index_bp.route('/contact-us')
def contact_us():
    return render_template('contact-us.html')

@index_bp.route('/event-details')
def event_details():
    form = TicketForm()
    # Pass current event id here or dynamically fill it in JS before showing modal
    return render_template('event-details.html', form=form)

@index_bp.route('/booking-history')
def booking_history():
    # Query all tickets with their user and event info
    tickets = Ticket.query.join(User).join(Event).all()
    
    return render_template('booking-history.html', tickets=tickets)

@index_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return render_template('index.html')

@index_bp.route('/book_ticket', methods=['GET', 'POST'])
@login_required
def book_ticket():
    form = TicketForm()

    if form.validate_on_submit():
        try:
            ticket = Ticket(
                user_id=int(form.user_id.data),
                event_id=int(form.event_id.data),
                number_of_tickets=int(form.number_of_tickets.data),
                tickets_type=form.tickets_type.data
            )
            db.session.add(ticket)
            db.session.commit()
            flash('Booking successful!', 'success')
            return redirect(url_for('index'))  # or your homepage/dashboard
        except ValueError:
            flash('Invalid data type submitted.', 'danger')

    return render_template('booking-history.html', form=form)

@index_bp.route('/add_comment', methods=['POST'])
@login_required
def add_comment():
    form = CommentForm()
    
    if form.validate_on_submit():
        try:
            comment = Comment(
                user_id=current_user.id,
                event_id=int(form.event_id.data),
                content=form.content.data
            )
            db.session.add(comment)
            db.session.commit()
            flash('Comment added successfully!', 'success')
            return redirect(url_for('index'))  # Redirect as needed
        except Exception as e:
            db.session.rollback()
            flash('Error adding comment.', 'danger')

    return render_template('event-detail.html', form=form)

@index_bp.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    
    if form.validate_on_submit():
        try:
            event = Event(
                title=form.title.data,
                description=form.description.data,
                date=form.date.data,
                creator_id=current_user.id
            )
            db.session.add(event)
            db.session.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating event.', 'danger')

    return render_template('create-event.html', form=form)
