from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from gerenciador_matriculas.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'gerentes.login'
login_manager.login_message = 'Você precisa fazer Login para acessar esta página'
login_manager.login_message_category = 'danger'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from gerenciador_matriculas.alunos.routes import alunos
    from gerenciador_matriculas.cursos.routes import cursos
    from gerenciador_matriculas.gerentes.routes import gerentes
    from gerenciador_matriculas.main.routes import main
    app.register_blueprint(alunos)
    app.register_blueprint(cursos)
    app.register_blueprint(gerentes)
    app.register_blueprint(main)

    return app
