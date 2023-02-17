from db import db

def get_comments(post_id):
    sql = "SELECT c.content, c.created_at, u.username, u.user_id FROM comments c JOIN users u ON c.user_id = u.user_id WHERE c.post_id = :post_id"
    result = db.session.execute(sql, {"post_id": post_id})
    comments = result.fetchall()
    return comments

def send_comment(user_id, post_id, content):
    if user_id == 0:
        return False
    sql = "INSERT INTO comments (user_id, post_id, content) VALUES (:user_id, :post_id, :content)"
    db.session.execute(sql, {"user_id":user_id, "post_id": post_id, "content": content})
    db.session.commit()
    return True


