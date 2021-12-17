from flask import json, jsonify, request, current_app, send_file
from sqlalchemy.sql.functions import user
from app.models.order_model import OrderModel
from http import HTTPStatus
from werkzeug.exceptions import NotFound
from app.utils.permission import permission_role
from app.exceptions.orders_exceptions import KeyTypeError, InvalidDate
import sqlalchemy
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.format_date import format_datetime
from app.utils.format_date import format_date_and_time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime


@jwt_required()
def list_orders():
    orders_list = OrderModel.query.all()
    return jsonify([{
        "id": order.id,
        "type": order.type.value,
        "status": order.status.value,
        "description": order.description,
        "release_date": order.release_date,
        "update_date": order.update_date,
        "solution": order.solution,
            "user": {
                "id": order.user.id,
                "name": order.user.name,
                "email": order.user.email,
                "position": order.user.position,
                "role": order.user.role.value,
            },
            "technician": order.technician,
    } for order in orders_list]), HTTPStatus.OK


@permission_role(('user', 'admin'))
@jwt_required()
def create_order():
    user_logged = get_jwt_identity()

    if 'position' not in user_logged.keys():
        return jsonify({"message": "only users to place an order"}), HTTPStatus.UNAUTHORIZED
    try:
        data = request.json
        data['user_id'] = user_logged['id']
        OrderModel.validate(data)
        verified_data = OrderModel.check_needed_keys(data)
        new_data = OrderModel.create_order_data(verified_data)
        order = OrderModel(**new_data)
        current_app.db.session.add(order)
        current_app.db.session.commit()

        return jsonify({
        "id": order.id,
        "type": order.type.value.title(),
        "status": order.status.value,
        "description": order.description,
        "release_date": order.release_date,
        "update_date": order.update_date,
        "solution": order.solution,
        "user": {
            "id": order.user.id,
            "name": order.user.name,
            "email": order.user.email,
            "position": order.user.position,
            "role": order.user.role.value,
        },
        "technician": order.technician,
    }), HTTPStatus.OK
    except InvalidDate as e:
        return jsonify({"message": str(e)}), HTTPStatus.BAD_REQUEST
    except KeyTypeError as e:
        return jsonify(e.message), e.code
    except sqlalchemy.exc.StatementError:
        return {"error":"Wrong field value"}


@jwt_required()
def get_order_by_id(id: int):
    try:
        order = OrderModel.query.get_or_404(id)
        return jsonify({
            "id": order.id,
            "type": order.type.value.title(),
            "status": order.status.value,
            "description": order.description,
            "release_date": order.release_date,
            "update_date": order.update_date,
            "solution": order.solution,
            "user": {
                "id": order.user.id,
                "name": order.user.name,
                "email": order.user.email,
                "position": order.user.position,
                "role": order.user.role.value,
            },
            "technician": order.technician,
                }), HTTPStatus.OK
    except NotFound:
        return {"Error": "Order not found."}, HTTPStatus.NOT_FOUND
    

@permission_role(('user', 'admin'))
@jwt_required()    
def update_order(id: int):
    user_logged = get_jwt_identity()
    if 'position' not in user_logged.keys():
        return jsonify({"message": "only users to place an order"}), HTTPStatus.UNAUTHORIZED
    try:
        data = request.get_json()
        order = OrderModel.query.filter_by(id=id).first()
        if not order:
            return jsonify({"msg": "order not found!"}), 404
        keys = ["type", "description"]
        for key, value in data.items():
        
                if key in keys:

                    setattr(order, key, value)
                else:
                    return jsonify({"msg": f"{key} field is wrong"}), 400
                    
        current_app.db.session.add(order)
        current_app.db.session.commit()
    except sqlalchemy.exc.DataError:
        return jsonify({"msg": "type value is wrong"}), 400
    
    return jsonify({
        "id": order.id,
        "type": order.type.value.title(),
        "status": order.status.value,
        "description": order.description,
        "release_date": order.release_date,
        "update_date": order.update_date,
        "solution": order.solution,
        "user": {
            "id": order.user.id,
            "name": order.user.name,
            "email": order.user.email,
            "position": order.user.position,
            "role": order.user.role.value,
        },
        "technician": order.technician,
        }), 200


@jwt_required()
def get_order_by_status(order_status: str):
    try:
        orders= OrderModel.query.filter_by(status=order_status).all()
       
        return jsonify([{
        "id": order.id,
        "type": order.type.value.title(),
        "status": order.status.value,
        "description": order.description,
        "release_date": order.release_date,
        "update_date": order.update_date,
        "solution": order.solution,
        "user": {
            "id": order.user.id,
            "name": order.user.name,
            "email": order.user.email,
            "position": order.user.position,
            "role": order.user.role.value,
        },
        "technician": order.technician,
            } for order in orders]), HTTPStatus.OK
    except NotFound:
        return {"Error": "Not found."}, HTTPStatus.NOT_FOUND


@permission_role(('user', 'admin'))
@jwt_required()    
def delete_order(id: int):
    user_logged = get_jwt_identity()
    try:
        order = OrderModel.query.get_or_404(id)
        if order.technician:
            return jsonify({"message": "order already assigned cannot be deleted"}), HTTPStatus.UNAUTHORIZED
        if 'position' not in user_logged.keys():
            return jsonify({"message": "only users to place an order"}), HTTPStatus.UNAUTHORIZED
        if user_logged['id'] != order.user_id:
            return jsonify({"message": "unauthorized delete order"}), HTTPStatus.UNAUTHORIZED
        current_app.db.session.delete(order)
        current_app.db.session.commit()
        return "", HTTPStatus.NO_CONTENT
    except NotFound:
        return {"message": "Not found."}, HTTPStatus.NOT_FOUND

@jwt_required()
def get_user_by_order_id(order_id):
    try:
        order = OrderModel.query.filter_by(id=order_id).first_or_404()
        return jsonify({
            "user": {
                "id": order.user.id,
                "name": order.user.name,
                "email": order.user.email,
                "birthdate": format_datetime(order.user.birthdate),
                "position": order.user.position,
                "role": order.user.role.value
            }
            
        }), HTTPStatus.OK
    except NotFound:
        return {"message": "Order not found!"}, HTTPStatus.NOT_FOUND


@jwt_required()
def get_technician_by_order_id(order_id):
    try:
        order = OrderModel.query.filter_by(id=order_id).first_or_404()
        if order.technician_id:
            return jsonify({
                "technician": {
                    "id": order.technician.id,
                    "name": order.technician.name,
                    "email": order.technician.email,
                    "birthdate": format_datetime(order.user.birthdate),
                }
            }), HTTPStatus.OK
        return jsonify({"message": "order was not assigned to a technician"}), HTTPStatus.NOT_FOUND
    except NotFound:
        return {"message": "Order not found!"}, HTTPStatus.NOT_FOUND


@permission_role(('super',))
@jwt_required()  
def create_pdf():
    try:
        orders = OrderModel.query.all()

        orders_list = []

        for order in orders:
            if order.status.value != "fechado":
                orders_list.append(order)

        if orders_list == []:
            raise NotFound

        cnv = canvas.Canvas("app/files/relatory/tech_relatory.pdf", pagesize=A4)

        cnv.drawImage("app/files/img/softclient.png", 0, 725, 150, 150)
        cnv.setFont("Helvetica", 14)
        cnv.drawString(450, 810, f"{format_date_and_time(datetime.now())}")
        cnv.setFont("Helvetica-Bold", 25)
        cnv.drawString(80, 720, "Relatório de pedidos não concluídos")
    
        cnv.setFont("Helvetica", 14)

        num_page = 1
        cnv.drawString(565, 20, f"{num_page}")

        y = 615
        for order in orders_list:
            cnv.drawString(80, y, f"Id: {order.id}")
            y -= 17
            cnv.drawString(80, y, f"Status: {order.status.value}")
            y -= 17
            cnv.drawString(80, y, f"Type: {order.type.value}")
            y -= 17
            cnv.drawString(80, y, f"Description: {order.description}")
            y -= 17
            cnv.drawString(80, y, f"Release_date: {format_date_and_time(order.release_date)}")
            y -= 17
            cnv.drawString(80, y, f"Update_date: {format_date_and_time(order.update_date)}")
            y -= 17
            cnv.drawString(80, y, f"User id: {order.user.id}")
            y -= 17
            cnv.drawString(80, y, f"User name: {order.user.name}")
            y -= 17
            cnv.drawString(80, y, f"User email: {order.user.email}")
            y -= 17
            cnv.drawString(80, y, f"Company id: {order.user.company.id}")
            y -= 17
            cnv.drawString(80, y, f"Company name: {order.user.company.trading_name}")

            if order.technician != None:
                y -= 17
                cnv.drawString(80, y, f"Technician id: {order.technician.id}")
                y -= 17
                cnv.drawString(80, y, f"Technician name: {order.technician.name}")
                y -= 17
                cnv.drawString(80, y, f"Technician email: {order.technician.email}")

            y -= 70

            if y < 200:
                cnv.showPage()
                cnv.setFont("Helvetica", 14)
                cnv.drawImage("app/files/img/softclient.png", 0, 725, 150, 150)
                cnv.drawString(450, 810, f"{format_date_and_time(datetime.now())}")
                num_page += 1
                cnv.drawString(565, 20, f"{num_page}")
                y = 660

        cnv.save()

        return send_file("files/relatory/tech_relatory.pdf", as_attachment=True), 200

    except NotFound:
        return jsonify({"msg": "The orders, for the moment, are all completed."}), 404
