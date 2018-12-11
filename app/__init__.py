from flask import Flask
from app.db import create_tables

create_tables.create_tables()
app = Flask(__name__)

app.url_map.strict_slashes = False

from app.api.v2.views import users, incident, api

app.register_blueprint(api, url_prefix='/api/v2')