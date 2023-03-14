from services.db import db

def get_comments(post_id):
    sql = "SELECT c.content, c.created_at, c.edited_at, u.username, u.user_id FROM comments c JOIN users u ON c.user_id = u.user_id WHERE c.post_id = :post_id ORDER BY c.created_at DESC"
    result = db.session.execute(sql, {"post_id": post_id})
    comments = result.fetchall()
    return comments

def get_comment(comment_id):
    sql = "SELECT content, created_at, edited_at, comment_id FROM comments WHERE comment_id = :comment_id"
    result = db.session.execute(sql, {"comment_id": comment_id})
    comment = result.fetchone()
    return comment

def get_users_comments(user_id):
    sql = "SELECT comment_id, content, created_at, edited_at, post_id FROM comments WHERE user_id = :user_id ORDER BY created_at DESC"
    result = db.session.execute(sql, {"user_id": user_id})
    comments = result.fetchall()
    return comments
    
def send_comment(user_id, post_id, content):
    if user_id == 0:
        return False
    sql = "INSERT INTO comments (user_id, post_id, content) VALUES (:user_id, :post_id, :content)"
    db.session.execute(sql, {"user_id":user_id, "post_id": post_id, "content": content})
    db.session.commit()
    return True

def delete_comment(comment_id, user_id):
    sql = "DELETE FROM comments WHERE comment_id = :comment_id AND user_id = :user_id"
    db.session.execute(sql, {"user_id": user_id, "comment_id": comment_id})
    db.session.commit()
    return True

def update_comment(comment_id, content, user_id):
    sql = "UPDATE comments SET content = :content, edited_at = CURRENT_TIMESTAMP WHERE comment_id = :comment_id AND user_id = :user_id"
    db.session.execute(sql, {"comment_id": comment_id, "user_id": user_id, "content": content})
    db.session.commit()
    return True
