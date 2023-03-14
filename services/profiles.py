from flask import session
from services.db import db
import services.auth as auth

def create_profile():
    user_id = auth.user_id()
    sql = "INSERT INTO profiles (user_id) VALUES (:user_id)"
    db.session.execute(sql, {"user_id":user_id})
    db.session.commit()
    
def get_profile(user_id):
    if user_id == 0:
        return False
    sql = "SELECT p.description, p.country, u.username FROM profiles p JOIN users u ON p.user_id = u.user_id WHERE u.user_id = :user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    profile = result.fetchone()
    return profile

def update_profile(description, country):
    user_id = auth.user_id()
    if user_id == 0:
        return False
    sql = "UPDATE profiles SET description=:description, country=:country WHERE user_id =:user_id"
    db.session.execute(sql, {"description":description, "country":country,"user_id":user_id})
    db.session.commit()
    return True