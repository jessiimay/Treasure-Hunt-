from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__,instance_relative_config=False)
    # db.init_app(app)
    # app.config.from_object(config.Config)
    app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://postgres:1747@localhost:5432/treasure_hunt'
    db = SQLAlchemy(app)

    with app.app_context():
        import routes

        db.create_all()
        print('@@@@@@')
        return app