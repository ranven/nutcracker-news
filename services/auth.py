from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from services.db import db

def signup(username, password):
    hash_value = generate_password_hash(password)

    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False

    return login(username, password)

def login(username, password):
    sql = "SELECT user_id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone() 

    if user:
        if check_password_hash(user.password, password):
            session["user_id"] = user.user_id
            session["username"] = username
            return True
    return False

def logout():
    del session["user_id"]
    del session["username"]
    
def user_id():
    return session.get("user_id", 0)
