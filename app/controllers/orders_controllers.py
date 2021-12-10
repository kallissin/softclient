from flask import jsonify, request, current_app
from sqlalchemy.sql.functions import user
from app.models.order_model import OrderModel
from pdb import set_trace
from http import HTTPStatus
from werkzeug.exceptions import NotFound


def list_orders():
    orders_list = OrderModel.query.all()
    # set_trace()
    return jsonify([{
        "type": order.type.value,
        "status": order.status.value,
        "description": order.description,
        "release_date": order.release_date,
        "update_date": order.update_date,
        "solution": order.solution,
        "user_id": order.user_id,
    } for order in orders_list]), 200



def create_order():
    data = request.json
    new_data = OrderModel.create_order_data(data)
    order = OrderModel(**new_data)
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

def get_order_by_id(id: int):
    try:
        order = OrderModel.query.get_or_404(id)
        return jsonify(order), 200
    except:
        return {"Error": "Order not found."}, 404
    

def delete_order(id: int):
    order = OrderModel.query.get_or_404(id)
    current_app.db.session.delete(order)
    current_app.db.session.commit()
    return jsonify(order), 200

def get_user_by_order_id(order_id):
    try:
        order = OrderModel.query.filter_by(id=order_id).first_or_404()
        return jsonify({
            "user": order.user
        }), HTTPStatus.OK
    except NotFound:
        return {"message": "Order not found!"}, HTTPStatus.NOT_FOUND


def get_technician_by_order_id(order_id):
    try:
        order = OrderModel.query.filter_by(id=order_id).first_or_404()
        return jsonify({
            "technician": order.technician
        }), HTTPStatus.OK
    except NotFound:
        return {"message": "Technician not found!"}, HTTPStatus.NOT_FOUND