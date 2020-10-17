from db import db
import armies_service

def get_user_matches(user_id):
    sql = "SELECT * FROM Match WHERE Match.User_id = :user_id AND Match.visible = 1"
    result = db.session.execute(sql, {"user_id": user_id})
    matches = result.fetchall()
    return matches

def find_match(match_id):
    sql = "SELECT * FROM Match WHERE Match.MatchId = :match_id"
    result = db.session.execute(sql, {"match_id": match_id})
    found_match = result.fetchone()
    return found_match

def find_match_by_name(match_name, user_id):
    sql = "SELECT * FROM Match " \
        "WHERE Match.Matchname = :match_name AND Match.User_id = :user_id"
    result = db.session.execute(sql, {"match_name": match_name, "user_id": user_id})
    found_match = result.fetchone()
    return found_match

def create_new(match_name, match_size, user_id):
    existing_match = find_match_by_name(match_name, user_id)
    if (existing_match == None):
        try:
            sql = "INSERT INTO Match (Matchname, Matchsize, User_Id) VALUES (:match_name, :match_size, :user_id)"
            db.session.execute(sql, {"match_name": match_name, "match_size": match_size, "user_id": user_id})
            db.session.commit()
            return True
        except:
            return False
    return False

def update_match(match_id, match_name, match_size, user_id):
    existing_match = find_match_by_name(match_name, user_id)
    if (existing_match == None or existing_match.matchid == match_id):
        try:
            sql = "UPDATE Match SET Matchname = :match_name, Matchsize = :match_size WHERE Match.MatchId = :match_id"
            db.session.execute(sql, {"match_name": match_name, "match_size": match_size, "match_id": match_id})
            db.session.commit()
            return True
        except:
            return False
    return False

def find_match_armies(match_id):
    sql = "SELECT army_id, army_side FROM matcharmy WHERE match_id = :match_id"
    result = db.session.execute(sql, {"match_id": match_id})
    armies = result.fetchall()
    force1 = []
    force2 = []
    
    for army in armies:
        if army[1] == 1:
            force1.append(armies_service.find_army(army[0]))
        else:
            force2.append(armies_service.find_army(army[0]))

    forces = []
    forces.append(force1)
    forces.append(force2)
    return forces

def add_army_to_match(match_id, army_id, army_side):
    try:
        sql = "INSERT INTO MatchArmy (Match_id, Army_id, Army_side) VALUES (:match_id, :army_id, :army_side)"
        db.session.execute(sql, {"match_id": match_id, "army_id": army_id, "army_side":army_side})
        db.session.commit()
    except:
        return False
    return True

def remove_army_from_match(match_id, army_id):
    try:
        sql = "DELETE FROM MatchArmy WHERE MatchArmy.Army_id = :army_id AND MatchArmy.Match_id = :match_id"
        db.session.execute(sql, {"army_id":army_id, "match_id":match_id})
        db.session.commit()
    except:
        return False
    return True