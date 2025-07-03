from flask import Flask
from extensions import db, jwt
from models import Facilitator, Event
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret'

    db.init_app(app)
    jwt.init_app(app)

    # Blueprint imports AFTER app/db initialized
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from routes.events import events_bp
    app.register_blueprint(events_bp)

    from routes.bookings import booking_bp
    app.register_blueprint(booking_bp)



    @app.route('/')
    def home():
        return 'Booking API is running.'

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        if not Facilitator.query.first():
            f1 = Facilitator()
            f1.name = "Alice"
            f1.crm_id = "crm_001"
            f2 = Facilitator()
            f2.name = "Bob"
            f2.crm_id = "crm_002"
            db.session.add_all([f1, f2])
            db.session.commit()

            e1 = Event()
            e1.name = "Yoga Retreat"
            e1.description = "A relaxing yoga session"
            e1.date = datetime(2025, 7, 10)
            e1.facilitator_id = f1.id
            e2 = Event()
            e2.name = "Mindfulness Session"
            e2.description = "Breathe. Reflect. Heal."
            e2.date = datetime(2025, 7, 20)
            e2.facilitator_id = f2.id
            db.session.add_all([e1, e2])
            db.session.commit()
    app.run(debug=True)
