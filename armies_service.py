from db import db
import units_service

def get_user_armies(user_id):
    sql = "SELECT * FROM Army WHERE Army.User_Id = :user_id AND Army.Visible = 1"
    result = db.session.execute(sql, {"user_id": user_id})
    return result

def get_user_hidden_armies(user_id):
    sql = "SELECT * FROM Army WHERE Army.User_Id = :user_id AND Army.Visible = 0"
    result = db.session.execute(sql, {"user_id": user_id})
    return result

def find_army(army_id):
    sql = "SELECT * FROM Army WHERE Army.ArmyId = :army_id AND Army.Visible = 1"
    result = db.session.execute(sql, {"army_id": army_id})
    found_army = result.fetchone()
    return found_army

def find_army_with_name_and_size(army_name, army_size, user_id):
    sql = "SELECT * FROM Army " \
        "WHERE Army.Armyname = :army_name AND Army.Armysize = :army_size AND Army.User_id = :user_id"
    result = db.session.execute(sql, {"army_name": army_name, "army_size": army_size, "user_id": user_id})
    found_army = result.fetchone()
    return found_army

def create_new(army_name, army_size, user_id):
    existing_army = find_army_with_name_and_size(army_name, army_size, user_id)
    if (existing_army != None):
        make_visible(existing_army[0])
        return existing_army[0]
    
    try:
        sql = "INSERT INTO Army (Armyname, Armysize, User_id) VALUES (:army_name, :army_size, :user_id) RETURNING ArmyId"
        result = db.session.execute(sql, {"army_name": army_name, "army_size": army_size, "user_id": user_id})
        new_id = result.fetchone()[0]
        db.session.commit()
    except:
        return False
    return new_id

def delete(army_id):
    try:
        sql = "UPDATE Army SET visible = 0 WHERE ArmyId = :army_id"
        db.session.execute(sql, {"army_id": army_id})
        db.session.commit()
    except:
        return False
    return True

def make_visible(army_id):
    try:
        sql = "UPDATE Army SET visible = 1 WHERE Army.ArmyId = :army_id"
        db.session.execute(sql, {"army_id": army_id})
        db.session.commit()
    except:
        return False
    return True

def find_army_units(army_id):
    sql = "SELECT Unit.UnitId, Unit.Unitname, Unit.Points, Unit.User_id, Unit.Visible FROM unit, armyunit " \
        "WHERE ArmyUnit.Army_id = :army_id AND ArmyUnit.Unit_id = Unit.UnitId"
    result = db.session.execute(sql, {"army_id": army_id})
    units = result.fetchall()
    fetchedUnits = []

    for unit in units:
        fetchedUnits.append(unit)

    return fetchedUnits

def add_unit_to_army(army_id, unit_id):
    try:
        sql = "INSERT INTO ArmyUnit (army_id, unit_id) VALUES (:army_id, :unit_id)"
        db.session.execute(sql, {"army_id": army_id, "unit_id": unit_id})
        db.session.commit()
    except:
        return False
    return True

def remove_unit_from_army(army_id, unit_id):
    try:
        sql = "DELETE FROM ArmyUnit WHERE ArmyUnit.Army_id = :army_id AND ArmyUnit.Unit_id = :unit_id"
        db.session.execute(sql, {"army_id": army_id, "unit_id": unit_id})
        db.session.commit()
    except:
        return False
    return True