from app import app
from flask import render_template, request, redirect
import users_service, matches_service, armies_service, units_service

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

@app.route("/addmatcharmy", methods=["POST"])
def addmatcharmy():
    match_id = request.form["match_id"]
    army_name = request.form["army_name"]
    army_size = request.form["army_size"]
    army_side = request.form["force"]
    new_or_existing_id = armies_service.create_new(army_name, army_size)
    if (new_or_existing_id != None):
        matches_service.add_army_to_match(match_id, new_or_existing_id, army_side)
    return redirect("/match/"+match_id)

@app.route("/armies", methods=["GET", "POST"])
def armies():
    if request.method == "GET":
        user_armies = armies_service.get_user_armies()
        return render_template("armies.html", armies=user_armies, message="")

    if request.method == "POST":
        army_name = request.form["army_name"]
        army_size = request.form["army_size"]
        armies_service.create_new(army_name, army_size)
        return redirect("/armies")

@app.route("/army/<int:army_id>", methods=["GET", "POST"])
def army(army_id):
    if request.method == "GET":
        selected_army = armies_service.find_army(army_id)
        included_units = armies_service.find_army_units(army_id)
        return render_template("army.html", army=selected_army, units=included_units, message="")

    if request.method == "POST":
        armies_service.delete(army_id)
        return redirect("/armies")

@app.route("/managearmyunits", methods=["POST"])
def managearmyunits():
    op_type = request.form["operation_type"]
    army_id = request.form["army_id"]

    if (op_type == "attach"):
        unit_name = request.form["unit_name"]
        unit_points = request.form["unit_points"]
        new_or_existing_id = units_service.create_new(unit_name, unit_points)
        if (new_or_existing_id != None):
            armies_service.add_unit_to_army(army_id, new_or_existing_id)
        return redirect("/army/"+army_id)

    if (op_type == "detach"):
        unit_id = request.form["unit_id"]
        armies_service.remove_unit_from_army(army_id, unit_id)
        return redirect("/army/"+army_id)

@app.route("/units", methods=["GET", "POST"])
def units():
    if request.method == "GET":
        user_units = units_service.get_user_units()
        user_hidden_units = units_service.get_user_hidden_units()
        return render_template("units.html", units=user_units, hidden_units=user_hidden_units, message="")

    if request.method == "POST":
        unit_name = request.form["unit_name"]
        unit_points = request.form["unit_points"]
        units_service.create_new(unit_name, unit_points)
        return redirect("/units")

@app.route("/unit/<int:unit_id>", methods=["POST"])
def unit(unit_id):
        units_service.delete(unit_id)
        return redirect("/units")