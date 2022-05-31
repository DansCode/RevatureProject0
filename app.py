from flask import Flask, render_template, request, make_response, redirect
from utilities import dbUtil

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def root_logic():
    if "authToken" in request.cookies:
        authToken = request.cookies.get("authToken")
        if dbUtil.checkToken(authToken):
            return render_template("board.html")

    return redirect("localhost:5000/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "authToken" in request.cookies:
        authToken = request.cookies.get("authToken")
        if dbUtil.checkToken(authToken):
            return redirect("localhost:5000")

    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        usr = request.form["username"]
        pwd = request.form["password"]

        auth = dbUtil.authenticate(usr, pwd)
        if auth is not None:
            response = make_response(redirect("localhost:5000"))
            response.set_cookie("authToken", auth)
            return response
        else:
            return render_template("systemMsg.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        usr = request.form["username"]
        pwd = request.form["password"]

        if dbUtil.register(usr, pwd):
            return redirect("localhost:5000")
        else:
            return render_template("systemMsg.html")
    

if __name__ == "__main__":
    app.run(debug=True)
