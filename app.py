from flask import Flask, render_template, request
from utilities import dbUtil

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def root_logic():
    if "authToken" in request.cookies:
        authToken = request.cookies.get("authToken")
        if dbUtil.checkToken(authToken):
            return render_template("board.html")

    return render_template("login.html")


@app.route("/register",methods=["GET","POST"])
def register():
    return render_template("register.html")


@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)
