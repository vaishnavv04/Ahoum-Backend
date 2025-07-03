from flask import Flask, render_template, redirect, request, session, url_for
from extensions import db, jwt
from models import Facilitator, Event
from datetime import datetime
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask_jwt_extended import decode_token
from models import User

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-fallback-key')

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from routes.auth import auth_bp
    from routes.events import events_bp
    from routes.bookings import booking_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(booking_bp)

    # Multi-page frontend routes
    @app.route('/')
    def home():
        return redirect('/login')

    @app.route('/login', methods=['GET'])
    def login_page():
        return render_template("login.html")

    @app.route('/register', methods=['GET'])
    def register_page():
        return render_template("register.html")

    @app.route('/logout')
    def logout():
        session.pop('token', None)
        return redirect('/login')


    @app.route('/dashboard', methods=['GET'])
    def dashboard():
        token = session.get("token")
        if not token:
            return redirect('/login')
        
        try:
            user_id = decode_token(token)["sub"]
            user = User.query.get(user_id)
            if not user:
                return redirect('/logout')
            return render_template("dashboard.html", token=token, user_name=user.name)
        except Exception:
            return redirect('/logout')

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
            f3 = Facilitator()
            f3.name = "Charlie"
            f3.crm_id = "crm_003"
            db.session.add_all([f1, f2, f3])
            db.session.commit()

            events = []
            e1 = Event()
            e1.name = "Yoga Retreat"
            e1.description = "Relax and stretch"
            e1.date = datetime(2025, 7, 10)
            e1.facilitator_id = f1.id
            events.append(e1)
            e2 = Event()
            e2.name = "Meditation Session"
            e2.description = "Find inner peace"
            e2.date = datetime(2025, 7, 15)
            e2.facilitator_id = f2.id
            events.append(e2)
            e3 = Event()
            e3.name = "Therapeutic Writing"
            e3.description = "Journaling to heal"
            e3.date = datetime(2025, 7, 18)
            e3.facilitator_id = f3.id
            events.append(e3)
            e4 = Event()
            e4.name = "Breathwork Intensive"
            e4.description = "Deep guided breathwork"
            e4.date = datetime(2025, 7, 20)
            e4.facilitator_id = f2.id
            events.append(e4)
            e5 = Event()
            e5.name = "Healing Circle"
            e5.description = "Group therapy with Charlie"
            e5.date = datetime(2025, 7, 25)
            e5.facilitator_id = f3.id
            events.append(e5)
            db.session.add_all(events)
            db.session.commit()

    app.run(debug=True)
