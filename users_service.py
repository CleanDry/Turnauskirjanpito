from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import os

def login(username, password):
    sql = "SELECT Password, UserId FROM Users WHERE Username = :username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user == None:
       return "Couldn't find user."
    else:
       if check_password_hash(user[0], password):
           session["user_id"] = user[1]
           session["username"] = username
           session["csrf_token"] = os.urandom(16).hex()
           return "Success"
       else:
           return "Incorrect username or password!"

def logout():
    del session["user_id"]
    del session["username"]
    del session["csrf_token"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO Users (Username, Password) VALUES (:username, :password)"
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except:
        return False
    return True

def user_id():
    return session.get("user_id",0)

def get_csrf_token():
    return session.get("csrf_token",0)