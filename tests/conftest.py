#!/usr/bin/env python3
import pytest
from flask import Flask
from flask.testing import FlaskClient

from calculate import create_app


@pytest.fixture
def client() -> FlaskClient:
    app: Flask = create_app()
    client: FlaskClient = app.test_client()
    return client
