from flask import request, jsonify, current_app
from app.exceptions.users_exceptions import InvalidBirthDateError, KeyTypeError
from app.models.user_model import UserModel
from http import HTTPStatus
from werkzeug.exceptions import NotFound
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

def format_datetime(date):
    return date.strftime('%d/%m/%Y')


def create_user():
    try:
        data = request.get_json()
        UserModel.validate_keys(data)
        user = UserModel(**data)

        current_app.db.session.add(user)
        current_app.db.session.commit()

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "birthdate": format_datetime(user.birthdate),
            "registration": user.registration,
            "role": user.role,
            "company_name": user.company.company_name
        }), HTTPStatus.CREATED
    except KeyTypeError as err:
        return jsonify(err.message), err.code
    except IntegrityError as err:
        if isinstance(err.orig, UniqueViolation):
            return jsonify({"message": str(err.orig).split('\n')[1]}), HTTPStatus.CONFLICT
    except InvalidBirthDateError as err:
        return jsonify({"message": str(err)}), HTTPStatus.BAD_REQUEST


def get_all_users():
    users = UserModel.query.all()

    for user in users:
        setattr(user, 'birthdate', format_datetime(user.birthdate))

    return jsonify(users), HTTPStatus.OK


def get_user_by_id(user_id):
    try:
        user = UserModel.query.filter_by(id=user_id).first_or_404()
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "birthdate": format_datetime(user.birthdate),
            "registration": user.registration,
            "role": user.role,
            "company_name": user.company.company_name
        }), HTTPStatus.OK
    except NotFound:
        return {"message": "user not found"}, HTTPStatus.NOT_FOUND


def update_user(user_id):
    data = request.get_json()
    user = UserModel.query.filter_by(id=user_id).first()
    for key, value in data.items():
        setattr(user, key, value)
    
    current_app.db.session.add(user)
    current_app.db.session.commit()
    
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "birthdate": format_datetime(user.birthdate),
        "registration": user.registration,
        "role": user.role,
        "company_name": user.company.company_name
    }), HTTPStatus.OK


def delete_user(user_id):
    try:
        user = UserModel.query.filter_by(id=user_id).first_or_404()
        current_app.db.session.delete(user)
        current_app.db.session.commit()
        return jsonify(user), HTTPStatus.OK
    except NotFound:
        return {"message": "user not found"}, HTTPStatus.NOT_FOUND


def get_company_by_user_id(user_id):
    try:
        user = UserModel.query.filter_by(id=user_id).first_or_404()
        return jsonify({
            "company": user.company
        }), HTTPStatus.OK
    except NotFound:
        return {"message": "user not found"}, HTTPStatus.NOT_FOUND