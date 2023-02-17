from db import db

def get_all_posts(user_id):
    if user_id == 0:
        sql = """SELECT p.title, p.content, p.created_at, p.post_id, u.user_id, u.username, 
        (SELECT COALESCE(SUM((v.vote_code)::int)-SUM((not v.vote_code)::int), 0) as votes FROM votes v WHERE v.post_id = p.post_id),
        (SELECT COUNT(*) as comment_count FROM comments c WHERE c.post_id = p.post_id)
        FROM posts p
        LEFT JOIN users u ON p.user_id = u.user_id
        LEFT JOIN votes v ON v.post_id = p.post_id
        GROUP BY(p.post_id, u.user_id, p.created_at)
        """
    else:
        sql = """SELECT p.title, p.content, p.created_at, p.post_id, u.user_id, u.username,
        (SELECT vc.vote_code FROM votes vc WHERE vc.post_id = p.post_id and vc.user_id = (:user_id)) as has_voted, 
        (SELECT COALESCE(SUM((v.vote_code)::int)-SUM((not v.vote_code)::int), 0) as votes FROM votes v WHERE v.post_id = p.post_id),
        (SELECT COUNT(*) as comment_count FROM comments c WHERE c.post_id = p.post_id)
        FROM posts p
        LEFT JOIN users u ON p.user_id = u.user_id
        LEFT JOIN votes v ON v.post_id = p.post_id AND v.user_id != (:user_id)
        GROUP BY(p.post_id, u.user_id, p.created_at)
        """
    result = db.session.execute(sql, {"user_id": user_id})
    posts = result.fetchall()
    return posts

def get_post(user_id, post_id):
    if user_id == 0:
        sql = """SELECT p.title, p.content, p.created_at, p.post_id, u.user_id, u.username, 
        (SELECT COALESCE(SUM((v.vote_code)::int)-SUM((not v.vote_code)::int), 0) as votes FROM votes v WHERE v.post_id = p.post_id) 
        FROM posts p
        LEFT JOIN users u ON p.user_id = u.user_id
        LEFT JOIN votes v ON v.post_id = p.post_id
        WHERE p.post_id = :post_id
        GROUP BY(p.post_id, u.user_id, p.created_at)
        """
    else:
        sql = """SELECT p.title, p.content, p.created_at, p.post_id, u.user_id, u.username,
        (SELECT vc.vote_code FROM votes vc WHERE vc.post_id = p.post_id and vc.user_id = (:user_id)) as has_voted, 
        (SELECT COALESCE(SUM((v.vote_code)::int)-SUM((not v.vote_code)::int), 0) as votes FROM votes v WHERE v.post_id = p.post_id) 
        FROM posts p
        LEFT JOIN users u ON p.user_id = u.user_id
        LEFT JOIN votes v ON v.post_id = p.post_id AND v.user_id != (:user_id)
        WHERE p.post_id = :post_id
        GROUP BY(p.post_id, u.user_id, p.created_at)
        """
    result = db.session.execute(sql, {"user_id":user_id, "post_id": post_id})
    post = result.fetchone()
    return post

def get_users_posts(user_id):
    sql = "SELECT title, content, created_at, post_id FROM posts WHERE user_id = :user_id"
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

