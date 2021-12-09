from flask import request, current_app, jsonify
from app.exceptions.companies_exceptions import CNPJFormatError, InvalidTokenError, InvalidIDError
from app.utils.cnpj_validator import is_cnpj_valid, cnpj_formatter
from app.models.companies_model import CompanyModel
from app.models.key_model import KeysModel

# RETURNS ALL COMPANIES
def get_all():
    company = CompanyModel.query.all()
    new_list = []
    
    for item in company:
        formatted_item = {
        "id": item.id,
        "cnpj": cnpj_formatter(item.cnpj),
        "trading_name": item.trading_name,
        "company_name": item.company_name,
        # "users": [] - Adicionar lista de usuários mais tarde
        }
        new_list.append(formatted_item)   
    
    return jsonify(new_list)


# RETURNS A SINGLE COMPANY BY ID
def get_one(company_id: int):
    company = CompanyModel.query.filter_by(id = company_id).first()
    
    if not company:
        return { "error": "Company not found."}, 404
    
    return jsonify({
        "id": company.id,
        "cnpj": cnpj_formatter(company.cnpj),
        "trading_name": company.trading_name,
        "company_name": company.company_name,
    }), 200


# DELETES A SINGLE COMPANY BY ID       
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
       
       
# CREATES A SINGLE COMPANY      
def create_company():
    session = current_app.db.session

    data = request.get_json()
    cnpj_check = is_cnpj_valid(data['cnpj'])
    
    
    try:
        if not cnpj_check:
            print(cnpj_check)
            raise CNPJFormatError

        data = {
            "cnpj": data['cnpj'],
            "trading_name": data['trading_name'].title(),
            "company_name": data['company_name'].title(),
            "username": None,
            "password": None,
            "role": None
        }
        
        new_company = CompanyModel(**data)

        session.add(new_company)
        session.commit()
        
    except CNPJFormatError as err:
        return err.message    
    
    return jsonify({
        "id": new_company.id,
        "cnpj": cnpj_formatter(new_company.cnpj),
        "trading_name": new_company.trading_name,
        "company_name": new_company.company_name,
    }), 201