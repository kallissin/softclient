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
        fail('Verifique se a rota "api/order<order_id>" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/api/order", essa rota não é capaz de processar uma requisição')


def teste_route_order_specific_user_exists(route_matcher):
    try:
        assert route_matcher("/api/order/1/user")
    except NotFound:
        fail('Verifique se a rota "api/order<order_id>/user" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/api/order", essa rota não é capaz de processar uma requisição')


def teste_route_order_specific_user_exists(route_matcher):
    try:
        assert route_matcher("/api/order/1/technicians")
    except NotFound:
        fail('Verifique se a rota "api/order<order_id>/technicians" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/api/order", essa rota não é capaz de processar uma requisição')