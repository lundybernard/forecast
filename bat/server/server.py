from flask import Flask
import connexion

from bat.lib import hello_world

app = Flask(__name__)


@app.route("/")
def hello_api():
    return hello_world()


def start_server(host="0.0.0.0", port=5000):
    app.run(host=host, port=port)


def start_api_server(host="0.0.0.0", port: int = 5000):
    app = connexion.FlaskApp(__name__, specification_dir="../api/")
    app.add_api("api.yaml")
    app.run(host=host, port=port)
