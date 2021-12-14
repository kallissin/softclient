from flask import jsonify, request, current_app
from sqlalchemy.sql.functions import user
from app.models.order_model import OrderModel
from http import HTTPStatus
from werkzeug.exceptions import NotFound
from app.utils.format_date import format_datetime
from app.exceptions.orders_exceptions import KeyTypeError
import sqlalchemy
from datetime import datetime


def list_orders():
    orders_list = OrderModel.query.all()
    # set_trace()
    return jsonify([{
        "id": order.id,
        "type": order.type.value,
        "status": order.status.value,
        "description": order.description,
        "release_date": order.release_date,
        "update_date": order.update_date,
        "solution": order.solution,
        "user_id": order.user_id,
        "technician_id": order.technician_id
    } for order in orders_list]), 200


def create_order():
    try:
        data = request.json
        OrderModel.validate(data)
        verified_data = OrderModel.check_needed_keys(data)
        new_data = OrderModel.create_order_data(verified_data)
        order = OrderModel(**new_data)
        current_app.db.session.add(order)
        current_app.db.session.commit()
    except KeyTypeError as e:
        return jsonify(e.message), e.code
    except sqlalchemy.exc.StatementError:
        return {"error":"Wrong field value"}

    return jsonify({
        "type": order.type.value,
        "status": order.status.value,
        "description": order.description,
        "release_date": order.release_date,
        "update_date": order.update_date,
        "solution": order.solution,
        "user_id": order.user.id,
        "technician_id": order.technician_id,
    }), 200

def get_order_by_id(id: int):
    try:
        order = OrderModel.query.get_or_404(id)
        return jsonify({
            "type": order.type.value,
            "status": order.status.value,
            "description": order.description,
            "release_date": order.release_date,
            "update_date": order.update_date,
            "solution": order.solution,
            "user_id": order.user.id,
            "technician_id": order.technician_id,
                }), 200
    except:
        return {"Error": "Order not found."}, 404
    
def update_order(order_id: int):
    data = request.get_json()
    order = OrderModel.query.get_or_404(id)
    
    
    keys = ["type", "description"]
        
    for key, value in data.items():

            if key in keys:

                setattr(order, key, value)
    
    current_app.db.session.add(order)
    current_app.db.session.commit()

    return jsonify({
        "type": order.type.value,
        "status": order.status.value,
        "description": order.description,
        "release_date": order.release_date,
        "update_date": order.update_date,
        "solution": order.solution,
        "user_id": order.user.id,
        "technician_id": order.technician_id,
    }), 200
    
 



def get_order_by_status(order_status: str):
    try:
        orders= OrderModel.query.filter_by(status=order_status).all()
       
        
        return jsonify([{
        "type": order.type.value,
        "status": order.status.value,
        "description": order.description,
        "release_date": order.release_date,
        "update_date": order.update_date,
        "solution": order.solution,
        "user_id": order.user_id,
        "technician_id": order.technician_id
            } for order in orders]), 200
    except:
        return {"Error": "Not found."}, 404
    
def delete_order(id: int):
    order = OrderModel.query.get_or_404(id)
    current_app.db.session.delete(order)
    current_app.db.session.commit()
    return "", 204
    

def get_user_by_order_id(order_id):
    try:
        order = OrderModel.query.filter_by(id=order_id).first_or_404()
        return jsonify({
            "user": {
                "id": order.user.id,
                "name": order.user.name,
                "email": order.user.email,
                "birthdate": format_datetime(order.user.birthdate),
                "registration": order.user.registration,
                "role": order.user.role
            }
            
        }), HTTPStatus.OK
    except NotFound:
        return {"message": "Order not found!"}, HTTPStatus.NOT_FOUND


def get_technician_by_order_id(order_id):
    try:
        order = OrderModel.query.filter_by(id=order_id).first_or_404()
        return jsonify({
            "technician": {
                "id": order.technician.id,
                "name": order.technician.name,
                "email": order.technician.email,
                "registration": order.user.registration,
                "birthdate": format_datetime(order.user.birthdate),
            }
        }), HTTPStatus.OK
    except NotFound:
        return {"message": "Technician not found!"}, HTTPStatus.NOT_FOUND