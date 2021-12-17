import click
from flask.cli import AppGroup
from flask import Flask, current_app
from werkzeug.exceptions import NotFound
from app.models.owner_model import OwnerModel
from app.models.companies_model import CompanyModel
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


def commands(app: Flask):
    cli = AppGroup('super')


    @cli.command('create')
    @click.argument('name')
    @click.argument('username')
    @click.argument('password')
    def create(name, username, password):
        try:
            owner = OwnerModel(name=name, username=username, password=password)

            current_app.db.session.add(owner)
            current_app.db.session.commit()

            return print(f'usuário {username} cadastrado')
        except IntegrityError as err:
            if isinstance(err.orig, UniqueViolation):
                return print("username already exists!")

    @cli.command('active')
    @click.argument('cnpj')
    def active(cnpj):
        username = str(input('username: '))
        password = str(input('password: '))
        try:
            owner = OwnerModel.query.filter_by(username=username).first_or_404()
            if owner.check_password(password):
                company = CompanyModel.query.filter_by(cnpj=cnpj).first()
                setattr(company, 'active', True)
                current_app.db.session.add(company)
                current_app.db.session.commit()
                return print('activated company')
        except NotFound:
            return print('username or password incorrect')
        
    app.cli.add_command(cli)


def init_app(app: Flask):
    commands(app)
