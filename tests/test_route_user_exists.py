from pytest import fail
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import InternalServerError


def teste_route_user_exists(route_matcher):
    try:
        assert route_matcher("/api/user")
    except NotFound:
        fail('Verifique se a rota "/user" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/api/user", essa rota não é capaz de processar uma requisição')


def teste_route_user_specific_exists(route_matcher):
    try:
        assert route_matcher("/api/user/1")
    except NotFound:
        fail('Verifique se a rota "/user/<user_id>" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/api/user", essa rota não é capaz de processar uma requisição')


def teste_route_user_specific_order_exists(route_matcher):
    try:
        assert route_matcher("/api/user/1/order")
    except NotFound:
        fail('Verifique se a rota "/user/<user_id>/order" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/api/user", essa rota não é capaz de processar uma requisição')


def teste_route_user_specific_company_exists(route_matcher):
    try:
        assert route_matcher("/api/user/1/company")
    except NotFound:
        fail('Verifique se a rota "/user/<user_id>/company" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/api/user", essa rota não é capaz de processar uma requisição')