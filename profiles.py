from flask import session
from db import db
import auth

def create_profile():
    user_id = auth.user_id()
    sql = "INSERT INTO profiles (user_id) VALUES (:user_id)"
    db.session.execute(sql, {"user_id":user_id})
    db.session.commit()
