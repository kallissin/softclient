from flask import request, current_app, jsonify
from app.exceptions.companies_exceptions import CNPJExistsError, FailedToLoginError, CNPJFormatError, CompanyNameExistsError, InvalidIDError, TradingNameExistsError
from app.utils.cnpj_validator import is_cnpj_valid, cnpj_formatter
from app.models.companies_model import CompanyModel
from app.models.user_model import UserModel
from flask_jwt_extended import create_access_token, jwt_required

from app.utils.permission import permission_role


# RETURNS ALL COMPANIES
@jwt_required()
def get_all():
    company = CompanyModel.query.all()
    new_list = []
    
    for item in company:
        users = UserModel.query.filter_by(company_id = item.id).all()
        formatted_item = {
        "id": item.id,
        "cnpj": cnpj_formatter(item.cnpj),
        "trading_name": item.trading_name,
        "company_name": item.company_name,
        "users": list(users)
        }
        new_list.append(formatted_item)   
    
    return jsonify(new_list)



# RETURNS A SINGLE COMPANY BY ID
@jwt_required()
def get_one(company_id: int):
    company = CompanyModel.query.filter_by(id = company_id).first()
    users = UserModel.query.filter_by(company_id = company.id).all()

    if not company:
        return { "error": "Company not found."}, 404
    
    return jsonify({
        "id": company.id,
        "cnpj": cnpj_formatter(company.cnpj),
        "trading_name": company.trading_name,
        "company_name": company.company_name,
        "users": list(users)
    }), 200
    


# GETS ALL USERS OF A GIVEN COMPANY
@jwt_required()         
def get_company_users(company_id: int):
    company = CompanyModel.query.filter_by(id = company_id).first()
    
    if not company:
        return { "error": "Company not found."}, 404
    
    users = UserModel.query.filter_by(company_id = company.id).all()
    
    return jsonify(users), 200



# DELETES A SINGLE COMPANY BY ID   
@jwt_required()    
def delete_company(company_id: int):
    try:
        query = CompanyModel.query.get(company_id)

        if not query:
            raise InvalidIDError

        current_app.db.session.delete(query)
        current_app.db.session.commit()

        return "", 204     
    
    except InvalidIDError as err:
        return err.message      



# UPDATES COMPANY
@permission_role('admin')
@jwt_required()
def update_company(company_id: int):
    session = current_app.db.session

    try:
        data = request.get_json()
        company = CompanyModel.query.get(company_id)
        
        if not company:
            raise InvalidIDError
        
        keys = ["cnpj", "trading_name", "company_name", "role", "username", "password"]
            
        for key, value in data.items():
            if key in keys:

                if key == "cnpj":
                    cnpj_check = is_cnpj_valid(value)                    
                    cnpj_exists_check = CompanyModel.query.filter_by(cnpj = key).first()
                    if not cnpj_check:
                        raise CNPJFormatError
                    if cnpj_exists_check:
                        raise CNPJExistsError
                        
                if key == "trading_name":
                    value = value.title()
                    trading_name_check = CompanyModel.query.filter_by(trading_name = value).first()
                    if trading_name_check:
                        raise TradingNameExistsError

                if key == "company_name":
                    value = value.title()
                    company_name_check = CompanyModel.query.filter_by(company_name = value).first()
                    if company_name_check:        
                        raise CompanyNameExistsError

                setattr(company, key, value)
            else:
                raise KeyError

        session.add(company)
        session.commit()

        return jsonify({
            "id": company.id,
            "cnpj": cnpj_formatter(company.cnpj),
            "trading_name": company.trading_name,
            "company_name": company.company_name,
    }), 200

    except InvalidIDError as err:
        return err.message
    except CNPJFormatError as err:
        return err.message
    except CNPJExistsError as err:
        return err.message
    except TradingNameExistsError as err:
        return err.message
    except CompanyNameExistsError as err:
        return err.message 
    except KeyError:
        return {
            "Error": f"Allowed keys are: {keys}"
        }, 400
        
        
        
       
# CREATES A SINGLE COMPANY      
def create_company():
    session = current_app.db.session

    data = request.get_json()
    cnpj_check = is_cnpj_valid(data['cnpj'])
    checklist = [ data['cnpj'], data['trading_name'].title(), data['company_name'].title() ]
    
    try:
        if not cnpj_check:
            raise CNPJFormatError
        
        
        cnpj_exists_check = CompanyModel.query.filter_by(cnpj = checklist[0]).first()
        if cnpj_exists_check:
            raise CNPJExistsError
        
        trading_name_check = CompanyModel.query.filter_by(trading_name = checklist[1]).first()
        if trading_name_check:
            raise TradingNameExistsError
        
        company_name_check = CompanyModel.query.filter_by(company_name = checklist[2]).first()
        if company_name_check:        
            raise CompanyNameExistsError
            
        data = {
            "cnpj": data['cnpj'],
            "trading_name": data['trading_name'].title(),
            "company_name": data['company_name'].title(),
            "username": data['username'],
            "password": data['password'],
            "role": 'admin',
            "active": False
        }
        
        new_company = CompanyModel(**data)

        session.add(new_company)
        session.commit()
        
    except CNPJFormatError as err:
        return err.message
    except CNPJExistsError as err:
        return err.message
    except TradingNameExistsError as err:
        return err.message
    except CompanyNameExistsError as err:
        return err.message    
    
    return jsonify({
        "id": new_company.id,
        "active": new_company.active,
        "cnpj": cnpj_formatter(new_company.cnpj),
        "trading_name": new_company.trading_name,
        "company_name": new_company.company_name,
    }), 201
    

@permission_role(('admin'))    
def login():
    data = request.get_json()
    password = data.pop('password')
    try:
        company: CompanyModel = CompanyModel.query.filter_by(username=data['username']).first()
        
        if not company:
            raise FailedToLoginError

        if company.check_password(password):
            return jsonify({"token": create_access_token(company)})
        
    except FailedToLoginError as err:
        return err.message  