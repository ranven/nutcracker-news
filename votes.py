from db import db

def send_vote(user_id, post_id, vote_code):
    if user_id == 0:
        return False
    sql = "INSERT INTO votes (user_id, post_id, vote_code) VALUES (:user_id, :post_id, :vote_code) ON CONFLICT (post_id, user_id) DO UPDATE SET vote_code = (:vote_code)"
    db.session.execute(sql, {"user_id":user_id, "post_id": post_id, "vote_code": vote_code})
    db.session.commit()
    return True
