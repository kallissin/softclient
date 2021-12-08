from pytest import fail
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import InternalServerError



def test_route_technicians_exists(route_matcher):
    try:
        assert route_matcher("/api/technicians")
    except NotFound:
        fail('Verifique se a rota "/api/technicians" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "api/technicians", essa rota não é capaz de processar uma requisição')


def test_route_technicians_specific_exists(route_matcher):
    try:
        assert route_matcher("/api/technicians/1")
    except NotFound:
        fail('Verifique se a rota "/api/technicians/<technicians_id>" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/api/technicians", essa rota não é capaz de processar uma requisição')


def test_route_technicians_specific_order_exists(route_matcher):
    try:
        assert route_matcher("/api/technicians/1/order")
    except NotFound:
        fail('Verifique se a rota "/api/technicians/<technicians_id>/order" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/api/technicians", essa rota não é capaz de processar uma requisição')