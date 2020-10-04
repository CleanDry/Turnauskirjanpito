from db import db
import users_service, units_service

def get_user_armies():
    user_id = users_service.user_id()
    sql = "SELECT * FROM Army WHERE Users.UserId = :userid AND Users.UserId = Match.User_id AND Match.MatchId = MatchArmy.Match_id AND MatchArmy.Army_id = Army.ArmyId"
    result = db.session.execute(sql, {"userid":user_id})
    return result

def find_army(id):
    sql = "SELECT * FROM Army WHERE Army.ArmyId=:army_id"
    result = db.session.execute(sql, {"army_id":id})
    found_army = result.fetchone()
    return found_army

def create_new(armyname, armysize):
    try:
        sql = "INSERT INTO Army (armyname, armysize) VALUES (:armyname,:armysize) RETURNING ArmyId"
        result = db.session.execute(sql, {"armyname":armyname, "armysize":armysize})
        new_id = result.fetchone()[0]
        db.session.commit()
    except:
        return False
    return new_id

def delete(ArmyId):
    try:
        sql = "UPDATE Units SET visible=0 WHERE ArmyId=:armyid"
        db.session.execute(sql, {"armyid":ArmyId})
        db.session.commit()
    except:
        return False
    return True

def find_army_units(army_id):
    user_id = users_service.user_id()
    if user_id == 0:
        return False
    sql = "SELECT unit_id FROM armyunit WHERE army_id=:army_id"
    result = db.session.execute(sql, {"army_id": army_id})
    unit_ids = result.fetchall()
    print("unit_ids", unit_ids)
    fetchedUnits = []

    for unit_id in unit_ids:
        fetchedUnits.append(units_service.find_unit(unit_id[0]))

    print("fetched units", fetchedUnits)
    return fetchedUnits

def add_unit_to_army(ArmyId, UnitId):
    try:
        sql = "INSERT INTO ArmyUnit (army_id, unit_id) VALUES (:armyid, :unitid)"
        db.session.execute(sql, {"armyid":ArmyId, "unitid":UnitId})
        db.session.commit()
    except:
        return False
    return True

def remove_unit_from_army(ArmyId, UnitId):
    try:
        sql = "DELETE * FROM ArmyUnit WHERE ArmyUnit.Army_id = :armyid AND ArmyUnit.Unit_id = :unitid"
        db.session.execute(sql, {"armyid":ArmyId, "unitid":UnitId})
        db.session.commit()
    except:
        return False
    return True

# Known issues
# 1. If army has multiple entries of a particular unit, remove_unit will remove all of them