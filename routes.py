from app import app
from flask import render_template, request, redirect
import users, user_matches

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", message="")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/matches")
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
            return redirect("/matches")
        else:
            return render_template("register.html", message="Incorrect username or password!")

@app.route("/matches", methods=["GET", "POST"])
def matches():
    if request.method == "GET":
        returned_matches = user_matches.get_matches()
        return render_template("matches.html", matches=returned_matches)
    if request.method == "POST":
        return render_template("index.html")