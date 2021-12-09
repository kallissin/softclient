from flask import request, jsonify, current_app
from app.models.user_model import UserModel


def create_user():
    data = request.get_json()
    
    user = UserModel(**data)

    current_app.db.session.add(user)
    current_app.db.session.commit()

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "birthdate": user.birthdate,
        "registration": user.registration,
        "role": user.role,
        "company_name": user.company.company_name
    })


def get_all_users():
    users = UserModel.query.all()

    list_users = [user for user in users]

    return jsonify(list_users)


def get_user_by_id(user_id):
    user = UserModel.query.filter_by(id=user_id).first()

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "birthdate": user.birthdate,
        "registration": user.registration,
        "role": user.role,
        "company_name": user.company.company_name
    })


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
        "birthdate": user.birthdate,
        "registration": user.registration,
        "role": user.role,
        "company_name": user.company.company_name
    })