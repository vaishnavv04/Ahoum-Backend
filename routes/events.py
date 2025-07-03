from flask import Blueprint, jsonify
from models import Event, Facilitator
from extensions import db
from flask_jwt_extended import jwt_required


events_bp = Blueprint('events', __name__, url_prefix='/events')

@events_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_events():
    events = Event.query.all()
    result = []
    for event in events:
        facilitator = Facilitator.query.get(event.facilitator_id)
        result.append({
            "id": event.id,
            "name": event.name,
            "description": event.description,
            "date": event.date.isoformat(),
            "facilitator": {
                "id": facilitator.id,
                "name": facilitator.name,
                "crm_id": facilitator.crm_id
            }
        })
    return jsonify(events=result)
