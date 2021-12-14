from flask import request, jsonify, current_app
from app.models.owner_model import OwnerModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound
from http import HTTPStatus


def create_owner():
    data = request.get_json()

    owner = OwnerModel(**data)

    current_app.db.session.add(owner)
    current_app.db.session.commit()

    return jsonify(owner)


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