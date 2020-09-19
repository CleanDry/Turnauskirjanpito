from db import db
import users_dao

def get_matches():
    user_id = users_dao.user_id()
    if user_id == 0:
        return False
    sql = "SELECT * FROM Match WHERE Match.User_id=:user_id AND Match.visible=1"
    result = db.session.execute(sql, {"user_id":user_id})
    matches = result.fetchall()
    return matches

def find_match(id):
    user_id = users_dao.user_id()
    if user_id == 0:
        return False
    sql = "SELECT * FROM Match WHERE Match.MatchId=:match_id"
    result = db.session.execute(sql, {"match_id":id})
    found_match = result.fetchone()
    return found_match

def create_new(match_name, match_size):
    user_id = users_dao.user_id()
    if user_id == 0:
        return False
    print("user_id", user_id)
    try:
        sql = "INSERT INTO Match (Matchname, Matchsize, User_Id) VALUES (:matchname, :matchsize, :userid)"
        db.session.execute(sql, {"matchname": match_name, "matchsize": match_size, "userid": user_id})
        db.session.commit()
    except:
        return False
    return True

def update_match(match_id, match_name, match_size):
    user_id = users_dao.user_id()
    if user_id == 0:
        return False
    try:
        sql = "UPDATE Match SET Matchname=:matchname, Matchsize=:matchsize WHERE MatchId=:matchid"
        db.session.execute(sql, {"matchname": match_name, "matchsize": match_size, "matchid": match_id})
        db.session.commit()
    except:
        return False
    return True

def delete_match(match_id):
    user_id = users_dao.user_id()
    if user_id == 0:
        return False
    try:
        sql = "UPDATE Match SET visible=0 WHERE MatchId=:matchid"
        db.session.execute(sql, {"matchid": match_id})
        db.session.commit()
    except:
        return False
    return True

def add_army_to_match(match_id, army_id, army_side):
    user_id = users_dao.user_id()
    if user_id == 0:
        return False
    try:
        sql = "INSERT INTO MatchArmy (Match_id, Army_id, Army_side) VALUES (:match_id, :army_id, :army_side)"
        db.session.execute(sql, {"match_id": match_id, "army_id": army_id, "army_side":army_side})
        db.session.commit()
    except:
        return False
    return True

def remove_army_from_match(match_id, army_id):
    user_id = users_dao.user_id()
    if user_id == 0:
        return False
    try:
        sql = "DELETE * FROM MatchArmy" \
                "WHERE MatchArmy.Army_id = :army_id" \
                "AND MatchArmy.Match_id = :match_id"
        db.session.execute(sql, {"armyid":army_id, "match_id":match_id})
        db.session.commit()
    except:
        return False
    return True