from flask import session
from db import db

def get_posts():
    sql = "SELECT p.post_id, p.title, p.content, p.created_at, u.username FROM POSTS p JOIN USERS u ON p.user_id = u.user_id"
    result = db.session.execute(sql)
    posts = result.fetchall()
    return posts

def submit_post(title, content, user_id):
    if user_id == 0:
        return False
    sql = "INSERT INTO posts (title, content, user_id) VALUES (:title, :content, :user_id)"
    db.session.execute(sql, {"title": title, "content": content, "user_id": user_id})
    db.session.commit()
    return True