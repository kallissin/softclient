from flask import request, jsonify, current_app
from app.models.technician_model import TechnicianModel
import sqlalchemy
import psycopg2
from werkzeug.exceptions import NotFound, BadRequest
from app.utils.cnpj_validator import cnpj_formatter
from app.utils.format_date import format_datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.exceptions import Unauthorized



def create_technician():
    try:
        data = request.get_json()

        if data["name"] and data["email"] and data["password"] and data["registration"]:

            if type(data["registration"]) != int:
                raise TypeError("the registration must be of the int type")
            
            if type(data["name"]) != str or type(data["email"]) != str or \
                    type(data["password"]) != str:
                raise TypeError("name, email and password key values ​​must be of type string.")

            data["name"] = data["name"].title()
            data["email"] = data["email"].lower()

            technician = TechnicianModel(**data)

            current_app.db.session.add(technician)
            current_app.db.session.commit()

            return jsonify({
                "id": technician.id,
                "name": technician.name,
                "email": technician.email,
                "registration": technician.registration,
                "birthdate": format_datetime(technician.birthdate)
            }), 200
            
        else:
            raise KeyError

    except sqlalchemy.exc.IntegrityError as e:
        if type(e.orig) == psycopg2.errors.UniqueViolation:
            return {"Error": "Technician already exists!"}, 409

    except KeyError:
        return {
            "Error": "It is mandatory to pass the name, email, password and registration keys."
        }, 400

    except BadRequest:
        return {"Error": "Syntax error!"}, 400

    except TypeError as e:
        return {"Error": str(e)}, 400




def get_technicians():
    technicians = TechnicianModel.query.all()
    return jsonify([{
        "id": technician.id,
        "name": technician.name,
        "email": technician.email,
        "registration": technician.registration,
        "birthdate": format_datetime(technician.birthdate)
    } for technician in technicians]), 200




def get_technician_by_id(id: int):
    try:
        technician = TechnicianModel.query.get_or_404(id)
        technician.birthdate = format_datetime(technician.birthdate)
        return jsonify(technician), 200
    except NotFound:
        return {"Error": "Technician not found."}, 404



@jwt_required()
def update_technician(id: int):
    try:
        data = request.get_json()

        technician = TechnicianModel.query.get_or_404(id)
        
        keys = ["name", "email", "password", "registration", "birthdate"]
            
        for key, value in data.items():

            if type(value) != str:
                raise TypeError

            if key in keys:

                if key == "name":
                    value = value.title()

                if key == "email":
                    value = value.lower()

                setattr(technician, key, value)
            else:
                raise KeyError

        current_app.db.session.add(technician)
        current_app.db.session.commit()

        return jsonify({
            "id": technician.id,
            "name": technician.name,
            "email": technician.email,
            "registration": technician.registration,
            "birthdate": format_datetime(technician.birthdate)
        }), 200

    except NotFound:
        return {"Error": "Technician not found."}, 404
    
    except sqlalchemy.exc.IntegrityError as e:
        if type(e.orig) == psycopg2.errors.UniqueViolation:
            return {"Error": "existing email or registration."}, 409
    
    except KeyError:
        return {
            "Error": "keys who can be updated: name, email, password, registration, birthdate."
        }, 400

    except TypeError:
        return {"Error": "the key value must be of type string."}, 400

    except BadRequest:
        return {"Error": "Syntax error!"}, 400



@jwt_required()
def delete_technician(id: int):

    token_compare = get_jwt_identity()

    try:
        technician = TechnicianModel.query.get_or_404(id)

        if id == token_compare["id"]:
            print("ok")

            current_app.db.session.delete(technician)
            current_app.db.session.commit()

            # technician.birthdate = format_datetime(technician.birthdate)

            return jsonify(technician), 200

            # return jsonify({
            #     "id": technician.id,
            #     "name": technician.name,
            #     "email": technician.email,
            #     "registration": technician.registration,
            #     "birthdate": format_datetime(technician.birthdate)
            # }), 200

    except NotFound:
        return {"Error": "Technician not found."}, 404




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
                "registration": order.user.registration,
                "role": order.user.role,
                "company": {
                    "id": order.user.company.id,
                    "cnpj": cnpj_formatter(order.user.company.cnpj),
                    "trading_name": order.user.company.trading_name
                }
            },
        } for order in technician.orders]), 200

    except NotFound:
        return {"Error": "Technician not found."}, 404



def login():
    try:
        data = request.get_json()

        technician = TechnicianModel.query.filter_by(email=data['email']).first()

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




