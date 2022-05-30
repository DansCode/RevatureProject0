from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def root_logic():
    authToken = request.cookies.get("authToken")
    return str(type(authToken))


if __name__ == "__main__":
    app.run(debug=True)
