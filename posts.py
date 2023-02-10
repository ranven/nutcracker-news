from flask import session
from db import db
import auth

def get_all_posts():
    sql = "SELECT p.post_id, p.title, p.content, p.created_at, u.username FROM POSTS p JOIN USERS u ON p.user_id = u.user_id"
    result = db.session.execute(sql)
    posts = result.fetchall()
    return posts

def get_users_posts(user_id):
    sql = "SELECT title, content, created_at FROM posts WHERE user_id = :user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    posts = result.fetchall()
    return posts

def submit_post(title, content, user_id):
    if user_id == 0:
        return False
    sql = "INSERT INTO posts (title, content, user_id) VALUES (:title, :content, :user_id)"
    db.session.execute(sql, {"title": title, "content": content, "user_id": user_id})
    db.session.commit()
    return True