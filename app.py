from flask import Flask, render_template, request
from utilities

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def root_logic():
    if "authToken" in request.cookies:
        authToken = request.cookies.get("authToken")

    return "lol"+str(type(authToken))


if __name__ == "__main__":
    app.run(debug=True)
