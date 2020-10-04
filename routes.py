from app import app
from flask import render_template, request, redirect
import users_service, matches_service, armies_service

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", message="")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users_service.login(username, password):
            return redirect("/matches")
        else:
            return render_template("index.html", message="Incorrect username or password!")

@app.route("/logout")
def logout():
    users_service.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", message="")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users_service.register(username,password):
            return redirect("/matches")
        else:
            return render_template("register.html", message="Incorrect username or password!")

@app.route("/matches", methods=["GET", "POST"])
def matches():
    if request.method == "GET":
        returned_matches = matches_service.get_matches()
        return render_template("matches.html", matches=returned_matches, message="")
    if request.method == "POST":
        match_name = request.form["match_name"]
        match_size = request.form["match_size"]
        if (matches_service.create_new(match_name, match_size)):
            return redirect("/matches")
        else:
            returned_matches = matches_service.get_matches()
            return render_template("matches.html", matches=returned_matches, message="Failed to create a new Match")

@app.route("/match/<int:id>", methods=["GET"])
def match(id):
    selected_match = matches_service.find_match(id)
    involvedForces = matches_service.find_match_armies(id)
    force1 = involvedForces[0]
    force2 = involvedForces[1]
    return render_template("match.html", match=selected_match, force1=force1, force2=force2, message="")

@app.route("/armies", methods=["POST"])
def armies():
    match_id = request.form["match_id"]
    army_name = request.form["army_name"]
    army_size = request.form["army_size"]
    army_side = request.form["force"]
    new_id = armies_service.create_new(army_name, army_size)
    if (new_id != None):
        matches_service.add_army_to_match(match_id, new_id, army_side)
    return redirect("/match/"+match_id)

@app.route("/match/<int:matchid>/army/<int:armyid>", methods=["GET"])
def army(matchid, armyid):
    selected_army = armies_service.find_army(armyid)
    includedUnits = armies_service.find_army_units(armyid)
    return render_template("army.html", matchid=matchid, army=selected_army, units=includedUnits, message="")