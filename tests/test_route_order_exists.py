from pytest import fail
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import InternalServerError


def teste_route_order_exists(route_matcher):
    try:
        assert route_matcher("/api/order")
    except NotFound:
        fail('Verifique se a rota "api/order" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/api/order", essa rota não é capaz de processar uma requisição')


def teste_route_order_specific_exists(route_matcher):
    try:
        assert route_matcher("/api/order/1")
    except NotFound:
        fail('Verifique se a rota "api/order/<order_id>" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/api/order", essa rota não é capaz de processar uma requisição')


def teste_route_order_specific_user_exists(route_matcher):
    try:
        assert route_matcher("/api/order/1/user")
    except NotFound:
        fail('Verifique se a rota "api/order/<order_id>/user" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/api/order", essa rota não é capaz de processar uma requisição')


def teste_route_order_specific_user_exists(route_matcher):
    try:
        assert route_matcher("/api/order/1/technicians")
    except NotFound:
        fail('Verifique se a rota "api/order/<order_id>/technicians" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/api/order", essa rota não é capaz de processar uma requisição')
