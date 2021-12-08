from flask import request, jsonify, current_app
from app.models.technician_model import TechnicianModel
import sqlalchemy
import psycopg2


def create_technician():
    try:
        data = request.get_json()

        if data["name"] and data["email"] and data["password"] and data["registration"]:

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



def get_all():

    technicians = TechnicianModel.query.all()

    return jsonify(technicians), 200
