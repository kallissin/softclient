from flask import request, jsonify, current_app
from app.exceptions.users_exceptions import InvalidBirthDateError, KeyTypeError
from app.models.user_model import UserModel
from app.models.order_model import OrderModel
from http import HTTPStatus
from werkzeug.exceptions import NotFound
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required
from app.utils.permission import only_role


def format_datetime(date):
    return date.strftime('%d/%m/%Y')


@only_role('admin')
@jwt_required()
def create_user():
    try:
        data = request.get_json()
        UserModel.validate_keys(data)
        new_data = UserModel.format_data(data)
        user = UserModel(**new_data)

        current_app.db.session.add(user)
        current_app.db.session.commit()

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "birthdate": format_datetime(user.birthdate),
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


@jwt_required()
def get_all_users():
    users = UserModel.query.all()

    for user in users:
        setattr(user, 'birthdate', format_datetime(user.birthdate))

    return jsonify([{
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "birthdate": user.birthdate,
        "role": user.role,
        "company": {
            "id": user.company.id,
            "trading_name": user.company.trading_name,
            "cnpj": user.company.cnpj
        }
    }for user in users]), HTTPStatus.OK


@jwt_required()
def get_user_by_id(user_id):
    try:
        user = UserModel.query.filter_by(id=user_id).first_or_404()
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "birthdate": format_datetime(user.birthdate),
            "role": user.role,
            "company": {
            "id": user.company.id,
            "trading_name": user.company.trading_name,
            "cnpj": user.company.cnpj
            }
        }), HTTPStatus.OK
    except NotFound:
        return {"message": "user not found"}, HTTPStatus.NOT_FOUND


@jwt_required()
def get_user_by_name(user_name):
    try:
        user = UserModel.query.filter_by(name=user_name.title()).first_or_404()
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "birthdate": format_datetime(user.birthdate),
            "role": user.role,
            "company": {
            "id": user.company.id,
            "trading_name": user.company.trading_name,
            "cnpj": user.company.cnpj
            }
        }), HTTPStatus.OK
    except NotFound:
        return {"message": "user not found"}, HTTPStatus.NOT_FOUND


@jwt_required()
def update_user(user_id):
    data = request.get_json()
    try:
        user = UserModel.query.filter_by(id=user_id).first_or_404()
        for key, value in data.items():
            setattr(user, key, value)
        
        current_app.db.session.add(user)
        current_app.db.session.commit()
        
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "birthdate": format_datetime(user.birthdate),
            "role": user.role,
            "company_name": user.company.company_name
        }), HTTPStatus.OK
    except NotFound:
        return {"message": "user not found"}, HTTPStatus.NOT_FOUND


@only_role('admin')
@jwt_required()
def delete_user(user_id):
    try:
        user = UserModel.query.filter_by(id=user_id).first_or_404()
        current_app.db.session.delete(user)
        current_app.db.session.commit()
        return jsonify(user), HTTPStatus.OK
    except NotFound:
        return {"message": "user not found"}, HTTPStatus.NOT_FOUND


@jwt_required()
def get_company_by_user_id(user_id):
    try:
        user = UserModel.query.filter_by(id=user_id).first_or_404()
        return jsonify({
            "company": {
                "id": user.company.id,
                "cnpj": user.company.cnpj,
                "trading_name": user.company.trading_name,
                "company_name": user.company.company_name
            }
        }), HTTPStatus.OK
    except NotFound:
        return {"message": "user not found"}, HTTPStatus.NOT_FOUN


@jwt_required()
def get_orders_by_user_id(user_id):
    try:
        orders_list = OrderModel.query.filter_by(id=user_id).all()
        return jsonify([{
        "id": order.id,
        "type": order.type.value,
        "status": order.status.value,
        "description": order.description,
        "release_date": order.release_date,
        "update_date": order.update_date,
        "solution": order.solution,
    }for order in orders_list]), HTTPStatus.OK

    except NotFound:
        return {"message": "user not found"}, HTTPStatus.NOT_FOUND
    

def login():
    data = request.get_json()
    password = data.pop('password')
    try:
        user: UserModel = UserModel.query.filter_by(email=data['email']).first_or_404()

        if user.check_password(password):
            return jsonify({"token": create_access_token(user)})
    except NotFound:
        return {"message": "user not found"}, HTTPStatus.NOT_FOUND
