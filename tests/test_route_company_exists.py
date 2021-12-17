from pytest import fail
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import InternalServerError


def teste_route_company_exists(route_matcher):
    try:
        assert route_matcher("/api/company")
    except NotFound:
        fail('Verifique se a rota "api/company" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/api/company", essa rota não é capaz de processar uma requisição')


def teste_route_company_specific_exists(route_matcher):
    try:
        assert route_matcher("/api/company/1")
    except NotFound:
        fail('Verifique se a rota "/api/company/<company_id>" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/api/company", essa rota não é capaz de processar uma requisição')


def teste_route_company_specific_user_exists(route_matcher):
    try:
        assert route_matcher("/api/company/1/user")
    except NotFound:
        fail('Verifique se a rota "/api/company/<company_id>/user" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/api/company", essa rota não é capaz de processar uma requisição')
