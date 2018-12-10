from flask import Flask

from app.db import create_tables
from app.api.v2.views import api

create_tables.create_tables()
app = Flask(__name__)

app.url_map.strict_slashes = False
app.register_blueprint(api, url_prefix='/api/v2')