from app import create_app, db
from flask import Flask, session, render_template
from flask_migrate import Migrate

app = create_app()

migrate = Migrate(app, db)

@app.route('/cause-error')
def cause_error():
    return 1 / 0  # This triggers ZeroDivisionError → 500
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.context_processor
def inject_user():
    return {
        'user_name': session.get('user_name'),
        'user_email': session.get('user_email')
    }

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)