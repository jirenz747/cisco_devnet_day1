from flask import Flask
from config import Config
import datetime
app = Flask(__name__)
app.config.from_object(Config)
app.permanent_session_lifetime = datetime.timedelta(days=1)

from app import routes





