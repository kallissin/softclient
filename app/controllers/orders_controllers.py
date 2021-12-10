from flask import jsonify, request, current_app
from app.models.order_model import OrderModel


def list_orders():
    orders_list = OrderModel.query.all()
    return jsonify(orders_list), 200

def create_order():
    data = request.json
    new_data = OrderModel.data_time(data)
    order = OrderModel(**new_data)
    current_app.db.session.add(order)
    current_app.db.session.commit()
    return jsonify(order), 200

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

    
   
