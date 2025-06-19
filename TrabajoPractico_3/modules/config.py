#dependencias
from flask import Flask
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import datetime

from modules.usuario import Usuario

# --- App y configuración general ---
# Crear instancia de Flask y definir la configuración
app = Flask("server")
app.config['SECRET_KEY'] = "d87h3dxodj09j30"
app.config["SESSION_TYPE"] = "filesystem" #guarda las sesiones en el sistema de archivos
app.config["SESSION_FILE_DIR"] = "./flask_session_cache" #carpeta donde se almacenan las sesione
app.config["SESSION_PERMANENT"] = False #False = la sesión termina cuando se cierra el navegador
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=15) #true = expira en 5 minutos


# --- SQLAlchemy engine ---
URL_BD = 'sqlite:///data/base_datos.db'

"""Crear el motor de conexión a la BD. 'crear_engine' devuelve
   una clase sesión de SQLAlchemy"""
def crear_engine():
    engine = create_engine(URL_BD)
    Session = sessionmaker(bind=engine)
    return Session

# --- Session filesystem ---
Session(app) #aplicar la configuración a la app

# --- Flask-Login ---
login_manager = LoginManager() #para manejar el login
login_manager.init_app(app) #conecta la app al flask-login
login_manager.login_view = "login" # para redirigir a la vista de login si no está autenticado
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."
login_manager.login_message_category = "error"


"""Cargar el usuario actual mediante id para Flask-Login 
   Devuelve una instancia del usuario"""
@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(int(user_id))

# --- Bootstrap ---
Bootstrap(app)