from db import db
import users_service

def get_user_units():
    user_id = users_service.user_id()
    sql = "SELECT * FROM Unit WHERE Unit.User_Id = :userid AND Unit.Visible = 1"
    result = db.session.execute(sql, {"userid": user_id})
    return result

def get_user_hidden_units():
    user_id = users_service.user_id()
    sql = "SELECT * FROM Unit WHERE Unit.User_Id = :userid AND Unit.Visible = 0"
    result = db.session.execute(sql, {"userid": user_id})
    return result

def find_unit(unit_id):
    sql = "SELECT * FROM Unit WHERE Unit.UnitId = :unit_id"
    result = db.session.execute(sql, {"unit_id": unit_id})
    found_unit = result.fetchone()
    return found_unit

def find_unit_with_name_and_points(unit_name, unit_points, user_id):
    sql = "SELECT * FROM Unit " \
        "WHERE Unit.Unitname = :unit_name AND Unit.Points = :unit_points AND Unit.User_id = :user_id"
    result = db.session.execute(sql, {"unit_name": unit_name, "unit_points": unit_points, "user_id": user_id})
    found_unit = result.fetchone()
    return found_unit

def create_new(unit_name, unit_points):
    user_id = users_service.user_id()
    if user_id == 0:
        return False
    existing_unit = find_unit_with_name_and_points(unit_name, unit_points, user_id)
    if (existing_unit != None):
        make_visible(existing_unit[0])
        return existing_unit[0]

    try:
        sql = "INSERT INTO Unit (Unitname, Points, User_id) VALUES (:unit_name, :unit_points, :user_id) RETURNING UnitId"
        result = db.session.execute(sql, {"unit_name": unit_name, "unit_points": unit_points, "user_id": user_id})
        new_id = result.fetchone()[0]
        db.session.commit()
    except:
        return False
    return new_id

def delete(unit_id):
    try:
        sql = "UPDATE Unit SET visible = 0 WHERE UnitId = :unit_id"
        db.session.execute(sql, {"unit_id": unit_id})
        db.session.commit()
    except:
        return False
    return True

def make_visible(unit_id):
    try:
        sql = "UPDATE Unit SET visible = 1 WHERE Unit.UnitId = :unit_id"
        db.session.execute(sql, {"unit_id": unit_id})
        db.session.commit()
    except:
        return False
    return True