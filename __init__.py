from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/weather'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    #Register blueprints
    from app.routes.main import main_bp
    from app.routes.historical import historical_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(historical_bp, url_prefix='/historical')
    
    return app