from flask import request, jsonify, current_app
from app.models.technician_model import TechnicianModel
import sqlalchemy
import psycopg2
from werkzeug.exceptions import NotFound, BadRequest



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

            return jsonify(technician), 200
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
    return jsonify(technicians), 200




def get_technician_by_id(id: int):
    try:
        technician = TechnicianModel.query.get_or_404(id)
        return jsonify(technician), 200
    except NotFound:
        return {"Error": "Technician not found."}, 404




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

        return jsonify(technician), 200

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




def delete_technician(id: int):
    try:
        technician = TechnicianModel.query.get_or_404(id)

        current_app.db.session.delete(technician)
        current_app.db.session.commit()

        return jsonify(technician), 200

    except NotFound:
        return {"Error": "Technician not found."}, 404


