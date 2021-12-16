from datetime import datetime
from flask import request, jsonify, current_app
from app.exceptions.technicians_exceptions import InvalidKeyError, OrderAlreadyTakenError
from app.models.technician_model import TechnicianModel
import sqlalchemy
import psycopg2
from werkzeug.exceptions import NotFound, BadRequest
from app.utils.cnpj_validator import cnpj_formatter
from app.utils.format_date import format_datetime, format_date_and_time
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.exceptions import Unauthorized
from app.models.order_model import OrderModel
from app.utils.permission import permission_role
    




@permission_role(('admin',))
def create_technician():
    try:
        data = request.get_json()

        if data["name"] and data["email"] and data["password"]:

            keys = ["name", "email", "password", "birthdate"]

            for key, value in data.items():
                if not key in keys:
                    raise InvalidKeyError
                if type(value) != str:
                    raise TypeError

            data["name"] = data["name"].title()
            data["email"] = data["email"].lower()

            technician = TechnicianModel(**data)

            current_app.db.session.add(technician)
            current_app.db.session.commit()

        else:
            raise KeyError

        for key, value in data.items():
            if key == "birthdate":
                technician.birthdate = format_datetime(technician.birthdate)

        return jsonify(technician), 200

    except sqlalchemy.exc.IntegrityError as e:
        if type(e.orig) == psycopg2.errors.UniqueViolation:
            return {"Error": "Technician already exists!"}, 409

    except KeyError:
        return {"Error": "It is mandatory to pass the name, email, and password keys."}, 400

    except BadRequest:
        return {"Error": "Syntax error!"}, 400

    except TypeError:
        return {"Error": "values ​​must be of type string"}, 400

    except InvalidKeyError:
        return {"Error": "Only name, email, password and birthday keys are accepted."}, 400

    except sqlalchemy.exc.DataError as e:
        if type(e.orig) == psycopg2.errors.InvalidDatetimeFormat:
            return {"Error": "Formato de data inválida. Use: (%d/%m/%Y)"}



@jwt_required()
def get_technicians():
    technicians = TechnicianModel.query.order_by(
        TechnicianModel.id.desc()).all()
    for technician in technicians:
        if technician.birthdate != None:
            technician.birthdate = format_datetime(technician.birthdate)
    return jsonify(technicians), 200



@jwt_required()
def get_technician_by_id(id: int):
    try:
        technician = TechnicianModel.query.get_or_404(id)

        if technician.birthdate != None:
            technician.birthdate = format_datetime(technician.birthdate)

        return jsonify(technician), 200

    except NotFound:
        return {"Error": "Technician not found."}, 404




@jwt_required()
def get_orders_by_technician(id: int):
    try:
        technician = TechnicianModel.query.get_or_404(id)

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
                "company": {
                    "id": order.user.company.id,
                    "cnpj": cnpj_formatter(order.user.company.cnpj),
                    "trading_name": order.user.company.trading_name
                }
            },
        } for order in technician.orders]), 200

    except NotFound:
        return {"Error": "Technician not found."}, 404




@jwt_required()
def update_technician(id: int):

    id_compared = get_jwt_identity()["id"]

    try:
        if id == id_compared:

            data = request.get_json()

            technician = TechnicianModel.query.get_or_404(id)

            keys = ["name", "email", "password", "birthdate"]

            for key, value in data.items():

                if key in keys:

                    if key == "name":
                        value = value.title()

                    if key == "email":
                        value = value.lower()

                    setattr(technician, key, value)
                else:
                    raise KeyError

                if type(value) != str:
                    raise TypeError

            current_app.db.session.add(technician)
            current_app.db.session.commit()

            technician.birthdate = format_datetime(technician.birthdate)

            return jsonify(technician), 200

        else:
            raise Unauthorized

    except NotFound:
        return {"Error": "Technician not found."}, 404

    except sqlalchemy.exc.IntegrityError as e:
        if type(e.orig) == psycopg2.errors.UniqueViolation:
            return {"Error": "existing email"}, 409

    except KeyError:
        return {
            "Error": "keys who can be updated: name, email, password, birthdate."
        }, 400

    except TypeError:
        return {"Error": "the key value must be of type string."}, 400

    except BadRequest:
        return {"Error": "Syntax error!"}, 400

    except Unauthorized:
        return {
            "Error": "it is not allowed to update information from other technicians."
        }, 401

    except sqlalchemy.exc.DataError as e:
        if type(e.orig) == psycopg2.errors.InvalidDatetimeFormat:
            return {"Error": "Formato de data inválida. Use: (%d/%m/%Y)"}




@jwt_required()
def take_order(order_id):

    token_id = get_jwt_identity()["id"]

    try:
        order = OrderModel.query.get_or_404(order_id)
        
        if order.status.value == "aberto":

            setattr(order, "technician_id", token_id)
            setattr(order, "status", "em_atendimento")
            setattr(order, "update_date", datetime.utcnow())

            current_app.db.session.add(order)
            current_app.db.session.commit()

            return jsonify(
                {
                    "order": {
                        "id": order.id,
                        "status": order.status.value,
                        "type": order.type.value,
                        "description": order.description,
                        "release_date": order.release_date,
                        "update_date": order.update_date,
                        "user": {
                            "id": order.user.id,
                            "name": order.user.name,
                            "email": order.user.email,
                            "position": order.user.position,
                            "birthdate": format_datetime(order.user.birthdate)
                        }
                    }
                }
            ), 200

        else:
            raise OrderAlreadyTakenError           
    
    except NotFound:
        return {"Error": "Order not found"}, 404

    except OrderAlreadyTakenError: 
        return {"Error": "the order has already been taken"}, 400 




@jwt_required()
def finalize_order(order_id):  
    try:  
        solution = request.get_json()["solution"]

        for key in request.get_json().keys():
            if key != "solution":
                raise KeyError

        if type(solution) != str:
            raise ValueError

        order = OrderModel.query.get_or_404(order_id)

        if order.status.value != "fechado":

            token_id = get_jwt_identity()["id"]

            if token_id == order.technician_id:

                setattr(order, "status", "fechado")
                setattr(order, "update_date", datetime.utcnow())
                setattr(order, "solution", solution)

                current_app.db.session.add(order)
                current_app.db.session.commit()

                return jsonify(
                    {
                        "order": {
                            "id": order.id,
                            "status": order.status.value,
                            "type": order.type.value,
                            "description": order.description,
                            "release_date": order.release_date,
                            "update_date": order.update_date,
                            "solution": order.solution,
                            "user": {
                                "id": order.user.id,
                                "name": order.user.name,
                                "email": order.user.email,
                                "position": order.user.position,
                                "birthdate": format_datetime(order.user.birthdate)
                            }
                        }
                    }
                ), 200

            else:
                raise Unauthorized
        
        else:
            return {"message": "this order has already been completed"}, 400

    except Unauthorized:
        return {"Error": "Technician not allowed to complete the order"}, 401

    except KeyError:
        return {"Error": "only the use of the solution key is allowed"}, 400

    except BadRequest:
        return {"Error": "Sintax error"}, 400

    except TypeError:
        return {"Error": "You must pass the solution key in the request body"}, 400

    except ValueError:
        return {"Error": "Only string type values ​​are accepted"}, 400

    except NotFound:
        return {"Error": "Order not found"}, 404





def login():
    try:
        data = request.get_json()

        technician = TechnicianModel.query.filter_by(
            email=data['email']).first()

        if technician.check_password(data['password']):
            token = create_access_token(technician)
            return jsonify({"token": token}), 200
        else:
            raise Unauthorized

    except (AttributeError, Unauthorized):
        return {"message": "Incorrect email or password."}, 401

    except BadRequest:
        return {"Error": "Syntax error!"}, 400

    except KeyError:
        return {"Error": "Login needs email and password keys."}, 400
