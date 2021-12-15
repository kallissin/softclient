from flask import request, jsonify, current_app
from app.exceptions.owners_exceptions import KeyRequiredError
from app.models.owner_model import OwnerModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


def create_owner():
    data = request.get_json()
    try:
        OwnerModel.validate_keys(data)
        owner = OwnerModel(**data)

        current_app.db.session.add(owner)
        current_app.db.session.commit()

        return jsonify(owner)
    except KeyRequiredError as err:
        return jsonify(err.message), err.code
    except IntegrityError as err:
        if isinstance(err.orig, UniqueViolation):
            return jsonify({"message": "username already exists!"}), HTTPStatus.CONFLICT

@jwt_required()
def get_all_owner():
    list_owner = OwnerModel.query.all()
    return jsonify(list_owner)


def login():
    data = request.get_json()
    password = data.pop('password')
    try:
        user: OwnerModel = OwnerModel.query.filter_by(username=data['username']).first_or_404()

        if user.check_password(password):
            return jsonify({"token": create_access_token(user)})
    except NotFound:
        return {"message": "user not found"}, HTTPStatus.NOT_FOUND