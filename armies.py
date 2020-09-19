from db import db
import users

def get_user_armies():
    user_id = users.user_id()
    sql = "SELECT * FROM Army" \ 
            "WHERE Users.UserId = :userid" \
            "AND Users.UserId = Match.User_id" \
            "AND Match.MatchId = MatchArmy.Match_id" \
            "AND MatchArmy.Army_id = Army.ArmyId"
    result = db.session.execute(sql, {"userid":user_id})
    print("get_user_armies result:", result)
    return result

def create_new(armyname, armysize):
    try:
        sql = "INSERT INTO Units (armyname, armysize) VALUES (:armyname,:armysize)"
        db.session.execute(sql, {"armyname":armyname, "armysize":armysize})
        db.session.commit()
    except:
        return False
    return True

def delete(ArmyId):
    try:
        sql = "UPDATE Units SET visible=0 WHERE ArmyId=:armyid"
        db.session.execute(sql, {"armyid":ArmyId})
        db.session.commit()
    except:
        return False
    return True

def add_unit(ArmyId, UnitId):
    try:
        sql = "INSERT INTO ArmyUnit (army_id, unit_id) VALUES (:armyid, unitid)"
        db.session.execute()
        db.session.commit()
    except:
        return False
    return True

def remove_unit(ArmyId, UnitId):
    try:
        sql = "DELETE * FROM ArmyUnit" \
                "WHERE ArmyUnit.Army_id = :armyid" \
                "AND ArmyUnit.Unit_id = :unitid"
        db.session.execute(sql, {"armyid":ArmyId, "unitid":UnitId})
        db.session.commit()
    except:
        return False
    return True

# Known issues
# 1. If army has multiple entries of a particular unit, remove_unit will remove all of them