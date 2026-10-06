"""Prototype 0: prove the web framework and routing work."""
import os

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Xpense prototype is running"


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
