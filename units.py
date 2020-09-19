from db import db
import users

def get_user_units():
    user_id = users.user_id()
    sql = "SELECT * FROM Units" \ 
            "WHERE Users.UserId = :userid" \
            "AND Users.UserId = Match.User_id" \
            "AND Match.MatchId = MatchArmy.Match_id" \
            "AND MatchArmy.Army_id = Army.ArmyId" \
            "AND Army.ArmyId = ArmyUnit.Army_id" \
            "AND ArmyUnit.Unit_id = Unit.UnitId"
    result = db.session.execute(sql, {"userid":user_id})
    print("get_user_units result:", result)
    return result

def create_new(unitname, points):
    try:
        sql = "INSERT INTO Units (unitname, points) VALUES (:unitname,:points)"
        db.session.execute(sql, {"unitname":unitname, "points":points})
        db.session.commit()
    except:
        return False
    
    return True

def delete(UnitId):
    try:
        sql = "UPDATE Units SET visible=0 WHERE UnitId=:unitid"
        db.session.execute(sql, {"unitid":UnitId})
        db.session.commit()
    except:
        return False

    return True