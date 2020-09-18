from app import app
from flask import render_template, request, redirect
import users

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", message="")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/app")
        else:
            return render_template("index.html", message="Incorrect username or password!")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", message="")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username,password):
            return redirect("/app")
        else:
            return render_template("register.html", message="Incorrect username or password!")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/result", methods=["POST"])
def result():
    return render_template("result.html", name=request.form["name"])

@app.route("/page/<int:id>")
def page(id):
    return "Tämä on sivu "+str(id)