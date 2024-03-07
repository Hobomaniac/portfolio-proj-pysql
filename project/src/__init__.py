from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("src.config.Config")

from .models import db
db.init_app(app)

from .api import users, accounts, routes, labels, notes
app.register_blueprint(users.bp)
app.register_blueprint(accounts.bp)
app.register_blueprint(routes.bp)
app.register_blueprint(labels.bp)
app.register_blueprint(notes.bp)

@app.route("/")
def hello_world():
    return jsonify(hello="world")
