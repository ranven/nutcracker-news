from services.db import db

def get_all_posts(user_id, sort_param, search_term):
    if user_id == 0:
        sql = """SELECT p.title, p.content, p.created_at, p.edited_at, p.post_id, u.user_id, u.username, 
        (SELECT COALESCE(SUM((v.vote_code)::int)-SUM((not v.vote_code)::int), 0) as votes FROM votes v WHERE v.post_id = p.post_id),
        (SELECT COUNT(*) as comment_count FROM comments c WHERE c.post_id = p.post_id)
        FROM posts p
        LEFT JOIN users u ON p.user_id = u.user_id
        LEFT JOIN votes v ON v.post_id = p.post_id
        search
        GROUP BY(p.post_id, u.user_id, p.created_at)
        """
    else:
        sql = """SELECT p.title, p.content, p.created_at, p.edited_at, p.post_id, u.user_id, u.username,
        (SELECT vc.vote_code FROM votes vc WHERE vc.post_id = p.post_id and vc.user_id = (:user_id)) as vote_code, 
        (SELECT COALESCE(SUM((v.vote_code)::int)-SUM((not v.vote_code)::int), 0) as votes FROM votes v WHERE v.post_id = p.post_id),
        (SELECT COUNT(*) as comment_count FROM comments c WHERE c.post_id = p.post_id)
        FROM posts p
        LEFT JOIN users u ON p.user_id = u.user_id
        LEFT JOIN votes v ON v.post_id = p.post_id AND v.user_id != (:user_id)
        search
        GROUP BY(p.post_id, u.user_id, p.created_at)
        """
    # add order by-clause to sql statement
    sql += get_order_clause(sort_param)
    # add where-clause to sql statement
    sql = sql.replace('search', get_search_clause(search_term))
    try:
        result = db.session.execute(sql, {"user_id": user_id, "search_term": search_term})
        posts = result.fetchall()
        return posts
    except:
        db.session.close()
        return []

def get_post(user_id, post_id):
    if user_id == 0:
        sql = """SELECT p.title, p.content, p.created_at, p.edited_at, p.post_id, u.user_id, u.username, 
        (SELECT COALESCE(SUM((v.vote_code)::int)-SUM((not v.vote_code)::int), 0) as votes FROM votes v WHERE v.post_id = p.post_id) 
        FROM posts p
        LEFT JOIN users u ON p.user_id = u.user_id
        LEFT JOIN votes v ON v.post_id = p.post_id
        WHERE p.post_id = :post_id
        GROUP BY(p.post_id, u.user_id, p.created_at)
        """
    else:
        sql = """SELECT p.title, p.content, p.created_at, p.edited_at, p.post_id, u.user_id, u.username,
        (SELECT vc.vote_code FROM votes vc WHERE vc.post_id = p.post_id and vc.user_id = (:user_id)) as vote_code, 
        (SELECT COALESCE(SUM((v.vote_code)::int)-SUM((not v.vote_code)::int), 0) as votes FROM votes v WHERE v.post_id = p.post_id) 
        FROM posts p
        LEFT JOIN users u ON p.user_id = u.user_id
        LEFT JOIN votes v ON v.post_id = p.post_id AND v.user_id != (:user_id)
        WHERE p.post_id = :post_id
        GROUP BY(p.post_id, u.user_id, p.created_at)
        """
    try: 
        result = db.session.execute(sql, {"user_id":user_id, "post_id": post_id})
        post = result.fetchone()
        return post
    except:
        db.session.close()
        return ()

def get_users_posts(user_id):
    sql = "SELECT title, content, created_at, post_id FROM posts WHERE user_id = :user_id ORDER BY created_at DESC"
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

def delete_post(post_id, user_id):
    sql = "DELETE FROM posts WHERE post_id = :post_id AND user_id = :user_id"
    db.session.execute(sql, {"user_id": user_id, "post_id": post_id})
    db.session.commit()
    return True

def update_post(post_id, content, title, user_id):
    sql = "UPDATE posts SET content = :content, title = :title, edited_at = CURRENT_TIMESTAMP WHERE post_id = :post_id AND user_id = :user_id"
    db.session.execute(sql, {"post_id": post_id, "user_id": user_id, "content": content, "title": title})
    db.session.commit()
    return True

#helper functions

def get_order_clause(sort_param):
    order = "ORDER BY "
    match sort_param:
        case "new":
            order += "(p.edited_at, p.created_at) DESC"
        case "old":
            order += "(p.edited_at, p.created_at) ASC"
        case "votes":
            order += "votes DESC"
        case "comments":
            order += "comment_count DESC"
    return order

def get_search_clause(search_term):
    if len(search_term) > 0:
        search = 'WHERE strpos(title, :search_term)>0 OR p.content ~* :search_term'
    else:
        search = ''
    return search


