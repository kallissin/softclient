from flask import request, jsonify, current_app
from app.exceptions.users_exceptions import InvalidBirthDateError, InvalidRoleError, KeyTypeError
from app.models.companies_model import CompanyModel
from app.models.user_model import UserModel
from app.models.order_model import OrderModel
from http import HTTPStatus
from werkzeug.exceptions import NotFound
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.utils.permission import permission_role
from pdb import set_trace

def format_datetime(date):
    return date.strftime('%d/%m/%Y')


@permission_role(('admin',))
@jwt_required()
def create_user():
    user_logged = get_jwt_identity()

    try:
        data = request.get_json()
        data['active'] = True
        if user_logged['email']:
            user = UserModel.query.filter_by(id=user_logged['id']).first()
            company = CompanyModel.query.filter_by(id=user.company.id).first()
            data['company_id'] = company.id
        else:
            data['company_id'] = user_logged['id']
        
        UserModel.validate_keys(data)
        new_data = UserModel.format_data(data)
        user = UserModel(**new_data)

        current_app.db.session.add(user)
        current_app.db.session.commit()

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "position": user.position,
            "birthdate": format_datetime(user.birthdate),
            "active": user.active,
            "role": user.role.value,
            "company_name": user.company.company_name
        }), HTTPStatus.CREATED
    except NotFound:
        return jsonify({"message": "Company not found"}), HTTPStatus.NOT_FOUND
    except InvalidRoleError as err:
        return jsonify({"message": str(err)}), HTTPStatus.BAD_REQUEST
    except KeyTypeError as err:
        return jsonify(err.message), err.code
    except IntegrityError as err:
        if isinstance(err.orig, UniqueViolation):
            return jsonify({"message": "Email already exists"}), HTTPStatus.CONFLICT
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
        "position": user.position,
        "active": user.active,
        "birthdate": user.birthdate,
        "role": user.role.value,
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
            "position": user.position,
            "active": user.active,
            "birthdate": format_datetime(user.birthdate),
            "role": user.role.value,
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
            "position": user.position,
            "active": user.active,
            "birthdate": format_datetime(user.birthdate),
            "role": user.role.value,
            "company": {
            "id": user.company.id,
            "trading_name": user.company.trading_name,
            "cnpj": user.company.cnpj
            }
        }), HTTPStatus.OK
    except NotFound:
        return {"message": "user not found"}, HTTPStatus.NOT_FOUND


@permission_role(('admin', 'user'))
@jwt_required()
def update_user(user_id):
    logged = get_jwt_identity()
    data = request.get_json()
    try:
        user = UserModel.query.filter_by(id=user_id).first_or_404()
        for key, value in data.items():
            if key in ['active', 'role']:
                if logged['role'] == 'admin':
                    setattr(user, key, value)
                else:
                    return jsonify({"message": "Unauthorized to update role"}), HTTPStatus.UNAUTHORIZED
            setattr(user, key, value)
        
        current_app.db.session.add(user)
        current_app.db.session.commit()
        
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "position": user.position,
            "active": user.active,
            "birthdate": format_datetime(user.birthdate),
            "role": user.role.value,
            "company_name": user.company.company_name
        }), HTTPStatus.OK
    except InvalidRoleError as err:
        return jsonify({"message": str(err)}), HTTPStatus.BAD_REQUEST
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
        return {"message": "user not found"}, HTTPStatus.NOT_FOUND


@jwt_required()
def get_orders_by_user_id(user_id):
    try:
        orders_list = OrderModel.query.filter_by(user_id=user_id).all()
        return jsonify([{
        "id": order.id,
        "type": order.type.value,
        "status": order.status.value,
        "description": order.description,
        "release_date": order.release_date,
        "update_date": order.update_date,
        "solution": order.solution,
        } for order in orders_list]), HTTPStatus.OK

    except NotFound:
        return {"message": "user not found"}, HTTPStatus.NOT_FOUND
    

def login():
    data = request.get_json()
    password = data.pop('password')
    try:
        user: UserModel = UserModel.query.filter_by(email=data['email']).first_or_404()

        if user.check_password(password):
            return jsonify({"token": create_access_token({"id": user.id,
            "name": user.name,
            "email": user.email,
            "position": user.position,
            "active": user.active,
            "birthdate": format_datetime(user.birthdate),
            "role": user.role.value,
            "company_name": user.company.company_name})})
    except NotFound:
        return {"message": "user not found"}, HTTPStatus.NOT_FOUND
