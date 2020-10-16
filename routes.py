from app import app
from flask import render_template, request, redirect
import users_service, matches_service, armies_service, units_service, utils

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", message="")
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        print("un", username, "pw", password)
        if not (utils.validate_input(username, 3, 32) & utils.validate_input(password, 3, 32)):
            return render_template("index.html", message="Incorrect username or password!")
            
        message = users_service.login(username, password)
        if message == "Success":
            return redirect("/matches")
        else:
            return render_template("index.html", message=message)
            

@app.route("/logout")
def logout():
    if users_service.user_id:
        users_service.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", message="")
    if request.method == "POST":
        message = ""
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        
        if not (utils.validate_input(username, 3, 32) & utils.validate_input(password, 3, 32)):
            return render_template("register.html", message = "Username and password must be 3-32 characters and contain only letters and numbers.")
        
        if users_service.register(username,password):
            message = users_service.login(username, password)
            if message == "Success":
                return redirect("/matches")
            else:
                return render_template("index.html", message="Logging in user failed")
        else:
            return render_template("register.html", message="Username already taken")

@app.route("/matches", methods=["GET", "POST"])
def matches():
    if not users_service.user_id:
        return redirect("/")

    if request.method == "GET":
        returned_matches = matches_service.get_user_matches()
        return render_template("matches.html", matches=returned_matches, message="")
    if request.method == "POST":
        if users_service.get_csrf_token() != request.form["csrf_token"]:
            abort(403)

        match_name = request.form["match_name"].strip()
        match_size = request.form["match_size"].strip()
        if (matches_service.create_new(match_name, match_size)):
            return redirect("/matches")
        else:
            returned_matches = matches_service.get_user_matches()
            return render_template("matches.html", matches=returned_matches, message="Failed to create a new Match")

@app.route("/match/<int:id>", methods=["GET"])
def match(id):
    if not users_service.user_id:
        return redirect("/")

    selected_match = matches_service.find_match(id)
    involvedForces = matches_service.find_match_armies(id)
    force1 = involvedForces[0]
    force2 = involvedForces[1]
    return render_template("match.html", match=selected_match, force1=force1, force2=force2, message="")

@app.route("/managematcharmies", methods=["POST"])
def managematcharmies():
    if not users_service.user_id:
        return redirect("/")
    if users_service.get_csrf_token() != request.form["csrf_token"]:
        abort(403)

    op_type = request.form["operation_type"]
    match_id = request.form["match_id"]
    
    if (op_type == "attach"):
        army_name = request.form["army_name"].strip()
        army_size = request.form["army_size"].strip()
        army_side = request.form["force"]
        new_or_existing_id = armies_service.create_new(army_name, army_size)
        if (new_or_existing_id != None):
            matches_service.add_army_to_match(match_id, new_or_existing_id, army_side)
        return redirect("/match/"+match_id)
    
    if (op_type == "detach"):
        army_id = request.form["army_id"]
        matches_service.remove_army_from_match(match_id, army_id)
        return redirect("/match/"+match_id)

@app.route("/armies", methods=["GET", "POST"])
def armies():
    if not users_service.user_id:
        return redirect("/")

    if request.method == "GET":
        user_armies = armies_service.get_user_armies()
        user_hidden_armies = armies_service.get_user_hidden_armies()
        return render_template("armies.html", armies=user_armies, hidden_armies=user_hidden_armies, message="")

    if request.method == "POST":
        if users_service.get_csrf_token() != request.form["csrf_token"]:
            abort(403)

        army_name = request.form["army_name"].strip()
        army_size = request.form["army_size"].strip()
        armies_service.create_new(army_name, army_size)
        return redirect("/armies")

@app.route("/army/<int:army_id>", methods=["GET", "POST"])
def army(army_id):
    if not users_service.user_id:
        return redirect("/")

    if request.method == "GET":
        selected_army = armies_service.find_army(army_id)
        included_units = armies_service.find_army_units(army_id)
        return render_template("army.html", army=selected_army, units=included_units, message="")

    if request.method == "POST":
        if users_service.get_csrf_token() != request.form["csrf_token"]:
            abort(403)

        armies_service.delete(army_id)
        return redirect("/armies")

@app.route("/managearmyunits", methods=["POST"])
def managearmyunits():
    if not users_service.user_id:
        return redirect("/")
    if users_service.get_csrf_token() != request.form["csrf_token"]:
        abort(403)

    op_type = request.form["operation_type"]
    army_id = request.form["army_id"]

    if (op_type == "attach"):
        unit_name = request.form["unit_name"].strip()
        unit_points = request.form["unit_points"].strip()
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
    if not users_service.user_id:
        return redirect("/")

    if request.method == "GET":
        user_units = units_service.get_user_units()
        user_hidden_units = units_service.get_user_hidden_units()
        return render_template("units.html", units=user_units, hidden_units=user_hidden_units, message="")

    if request.method == "POST":
        if users_service.get_csrf_token() != request.form["csrf_token"]:
            abort(403)

        unit_name = request.form["unit_name"].strip()
        unit_points = request.form["unit_points"].strip()
        units_service.create_new(unit_name, unit_points)
        return redirect("/units")

@app.route("/unit/<int:unit_id>", methods=["POST"])
def unit(unit_id):
    if not users_service.user_id:
        return redirect("/")
    if users_service.get_csrf_token() != request.form["csrf_token"]:
        abort(403)

    units_service.delete(unit_id)
    return redirect("/units")