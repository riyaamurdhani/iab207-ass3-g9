from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.event import Event
from app.models.comment import Comment
from app.models.ticket import Ticket
from flask_login import login_required, current_user
from datetime import datetime

event_bp = Blueprint('event', __name__)

@event_bp.route('/event/create', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')

        event = Event(title=title, description=description, date=date, creator_id=current_user.id)
        db.session.add(event)
        db.session.commit()
        flash('Event created.', 'success')
        return redirect(url_for('index.dashboard'))
    return render_template('create_event.html')


@event_bp.route('/event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        content = request.form['comment']
        comment = Comment(content=content, user_id=current_user.id, event_id=event.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added.', 'success')
    return render_template('event_detail.html', event=event)


@event_bp.route('/event/<int:event_id>/buy', methods=['POST'])
@login_required
def buy_ticket(event_id):
    ticket = Ticket(user_id=current_user.id, event_id=event_id)
    db.session.add(ticket)
    db.session.commit()
    flash('Ticket purchased.', 'success')
    return redirect(url_for('event.event_detail', event_id=event_id))
