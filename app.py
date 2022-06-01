from flask import Flask, render_template, request, make_response, redirect
from utilities import dbUtil

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def root_logic():
    if "authToken" in request.cookies:
        authToken = request.cookies.get("authToken")
        if dbUtil.checkToken(authToken):
            if request.method == "GET":
                return render_template("board.html", posts=dbUtil.getPosts())
            elif request.method == "POST":
                msg = request.form["message"]
                dbUtil.makePost(authToken, msg)
                return render_template("board.html", posts=dbUtil.getPosts())

    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "authToken" in request.cookies:
        authToken = request.cookies.get("authToken")
        if dbUtil.checkToken(authToken):
            return redirect("/")

    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        usr = request.form["username"]
        pwd = request.form["password"]

        auth = dbUtil.authenticate(usr, pwd)
        if auth is not None:
            response = make_response(redirect("/"))
            response.set_cookie("authToken", auth)
            return response
        else:
            return render_template("systemMsg.html", message="error logging in")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        usr = request.form["username"]
        pwd = request.form["password"]

        if dbUtil.register(usr, pwd):
            return render_template("systemMsg.html", message="success")
        else:
            return render_template("systemMsg.html", message="error registering")


@app.route("/logout", methods=["GET"])
def logout():
    response = make_response(render_template("systemMsg.html", message="logged out"))
    response.delete_cookie("authToken")
    return response


@app.route("/deactivate")
def deactivate_account():
    if "authToken" in request.cookies:
        authToken = request.cookies.get("authToken")
        if dbUtil.checkToken(authToken):
            dbUtil.deactivate(authToken)
            response = make_response(render_template("systemMsg.html", message="account deactivated"))
            response.delete_cookie("authToken")
            return response

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
