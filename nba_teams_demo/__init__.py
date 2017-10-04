from flask import Flask
from nba_teams_demo.api.routes import api
from nba_teams_demo import settings
from nba_teams_demo.database import db

app = Flask(__name__)
# add prefix api to base url of the web service
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.register_blueprint(api, url_prefix='/api')
db.init_app(app)