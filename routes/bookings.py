from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from models import Booking, Event, User, Facilitator
from extensions import db
from crm.notify import notify_crm
from schemas import BookingSchema
from marshmallow import ValidationError

booking_bp = Blueprint('booking', __name__, url_prefix='/bookings')

@booking_bp.route('/', methods=['POST'])
@jwt_required()
def book_event():
    try:
        data = BookingSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    user_id = get_jwt_identity()
    event_id = data['event_id']

    event = Event.query.get(event_id)
    if not event:
        return jsonify({"msg": "Event not found"}), 404

    # Check for duplicate booking
    existing = Booking.query.filter_by(user_id=user_id, event_id=event_id).first()
    if existing:
        return jsonify({"msg": "You have already booked this event"}), 409

    booking = Booking()
    booking.user_id = user_id
    booking.event_id = event_id
    booking.timestamp = datetime.utcnow()
    db.session.add(booking)
    db.session.commit()

    user = User.query.get(user_id)
    facilitator = Facilitator.query.get(event.facilitator_id)

    notify_crm({
        "booking_id": booking.id,
        "event": {
            "id": event.id,
            "name": event.name,
            "date": event.date.isoformat()
        },
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        },
        "facilitator_crm_id": facilitator.crm_id
    })

    return jsonify({"msg": "Booking confirmed", "booking_id": booking.id}), 201

@booking_bp.route('/my', methods=['GET'])
@jwt_required()
def get_my_bookings():
    user_id = get_jwt_identity()
    bookings = Booking.query.filter_by(user_id=user_id).all()
    result = []
    for b in bookings:
        event = Event.query.get(b.event_id)
        result.append({
            "booking_id": b.id,
            "event": {
                "id": event.id,
                "name": event.name,
                "date": event.date.isoformat()
            },
            "timestamp": b.timestamp.isoformat()
        })
    return jsonify(bookings=result)
