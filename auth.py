from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db

def signup(username, password):
    hash_value = generate_password_hash(password)

    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()

    if login(username, password):
        return True
    return False

def login(username, password):
    sql = "SELECT user_id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone() 

    if user:
        if check_password_hash(user.password, password):
            session["user_id"] = user.user_id
            return True
    return False

def logout():
    del session["user_id"]
    
def user_id():
    return session.get("user_id", 0)