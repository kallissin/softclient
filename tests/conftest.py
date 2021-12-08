import pytest
from flask import Flask
from app import create_app


@pytest.fixture(scope="module")
def app():
    """Instance of main flask app"""
    return create_app()


@pytest.fixture
def route_matcher(app: Flask):
    return app.url_map.bind("").match
