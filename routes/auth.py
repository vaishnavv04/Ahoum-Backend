from flask import Blueprint, request, jsonify, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
from schemas import RegisterSchema, LoginSchema
from marshmallow import ValidationError

from extensions import db
from models import User


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        if request.is_json:
            data = RegisterSchema().load(request.get_json())
        else:
            data = {
                "name": request.form.get("name"),
                "email": request.form.get("email"),
                "password": request.form.get("password")
            }

        if User.query.filter_by(email=data['email']).first():
            return jsonify({"msg": "User already exists"}), 409

        hashed_pw = generate_password_hash(str(data['password']))
        new_user = User()
        new_user.name = data['name']
        new_user.email = data['email']
        new_user.password = hashed_pw
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=str(new_user.id), expires_delta=timedelta(days=1))

        if request.is_json:
            return jsonify({"msg": "User created", "access_token": access_token}), 201
        else:
            session['token'] = access_token
            return redirect('/dashboard')


    except ValidationError as err:
        return jsonify(err.messages), 400


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        if request.is_json:
            data = LoginSchema().load(request.get_json())
        else:
            # From HTML form
            data = {
                "email": request.form.get("email"),
                "password": request.form.get("password")
            }

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, str(password)):
            return jsonify({"msg": "Invalid credentials"}), 401

        access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))

        if request.is_json:
            return jsonify(access_token=access_token), 200
        else:
            session['token'] = access_token
            return redirect('/dashboard')

    except ValidationError as err:
        return jsonify(err.messages), 400
