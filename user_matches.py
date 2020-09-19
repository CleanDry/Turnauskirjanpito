from db import db
import users

def get_matches():
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "SELECT * FROM Match WHERE User_id=:user_id AND Match.visible=1"
    matches = db.session.execute(sql, {"user_id":user_id})
    print("matches", matches)
    return matches

def create_new_match(points, force1, force2):
    user_id = user_id()
    if user_id == 0:
        return False
    try:
        sql = ""
        db.session.execute(sql, params)
        db.session.commit()
    except:
        return False
    return True

# def update_match():
    # implement

# def remove_match():
    # implement