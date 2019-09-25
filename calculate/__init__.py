#!/usr/bin/env python3

from flask import Flask

from calculate import cal


def create_app():
    app = Flask(__name__)
    app.register_blueprint(cal.bp)
    return app
