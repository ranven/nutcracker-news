from app import app
from flask import abort, flash, session
from flask import render_template, request, redirect
import services.auth as auth
import services.posts as posts
import services.profiles as profiles
import services.votes as votes
import services.comments as comments
import services.helpers as helpers


@app.route("/")
def index():
    return redirect("/posts")

# auth
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if helpers.validate_length(username, "username") and auth.login(username, password):
            flash("Login successful!")
            return redirect("/posts")
        else:
            flash("Invalid password or username.")
            return redirect("/login")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if helpers.validate_password(password) and helpers.validate_length(username, "username"):
            if auth.signup(username, password):
                profiles.create_profile()
                flash("Successfully signed up!")
                return redirect("/posts")
            else:
                flash("This username is taken. Please try again")
                return redirect("/signup")
        else:
            flash("Username or password doesn't match requirements.")
            return redirect("/signup")


@app.route("/logout")
def logout():
    auth.logout()
    return redirect("/")

# posts


@app.route("/posts", methods=["POST", "GET"])
def post():
    authenticated_user = auth.user_id()
    if request.method == "GET":
        if request.args.get("sort_by"):
            sort_param = request.args.get("sort_by")
            search_term = request.args.get("search_term")
        else:
            sort_param = "new"
            search_term = ""
        try:
            all_posts = posts.get_all_posts(
                authenticated_user, sort_param, search_term)
            return render_template("posts.html", posts=all_posts, sort_by=sort_param)
        except:
            abort(500)

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        title = request.form["title"]
        content = request.form["content"]
        if helpers.validate_length(title, "post_title") and helpers.validate_length(content, "post_content"):
            if posts.submit_post(title, content, authenticated_user):
                flash("Post successfully created!")
                return redirect("/posts")
            else:
                flash("You need an account to post.")
                return redirect("login")
        else:
            flash("Maximum length of title or content exceeded.")


@app.route("/posts/<post_id>", methods=["GET"])
def get_post(post_id):
    authenticated_user = auth.user_id()
    post = posts.get_post(authenticated_user, post_id)
    post_comments = comments.get_comments(post_id)
    return render_template("post.html", post=post, post_comments=post_comments)


@app.route("/posts/create", methods=["GET"])
def create_post():
    if request.method == "GET":
        return render_template("create.html")

# comments


@app.route("/posts/<post_id>/comments", methods=["POST"])
def send_comment(post_id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    authenticated_user = auth.user_id()
    content = request.form["content"]
    if helpers.validate_length(content, "comment_content"):
        if comments.send_comment(authenticated_user, post_id, content):
            flash("Comment sent!")
            return redirect("/posts/"+post_id)
        else:
            flash("You need an account to comment.")
            return redirect("login")
    else:
        flash("Maximum length of content exceeded.")

# profiles


@app.route("/users/<user_id>", methods=["POST", "GET"])
def profile(user_id):
    is_admin = False
    authenticated_user = auth.user_id()

    if int(user_id) == authenticated_user:
        is_admin = True

    if request.method == "GET":
        profile = profiles.get_profile(user_id)
        users_posts = posts.get_users_posts(user_id)
        users_comments = comments.get_users_comments(user_id)
        return render_template("profile.html", profile=profile, posts=users_posts, comments=users_comments, admin=is_admin)

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if is_admin:
            description = request.form["description"]
            country = request.form["country"]
            if helpers.validate_length(description, "description") and helpers.validate_length(country, "country"):
                if profiles.update_profile(description, country):
                    flash("Profile successfully updated!")
                    return redirect("/users/"+user_id)
                else:
                    flash("You cannot edit someone else's profile.")
                    return redirect("/posts")
            else:
                flash("Maximum length of content exceeded.")

# votes


@app.route("/likes", methods=["POST"])
def send_vote():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    authenticated_user = auth.user_id()
    post_id = request.form["post_id"]
    vote_code = True if request.form["vote_button"] == "+1" else False
    if votes.send_vote(authenticated_user, post_id, vote_code):
        return redirect('/posts/'+post_id)
    else:
        flash("Error voting this post.")
        return redirect('/posts')

# edit/delete posts/comments


@app.route("/edit/<content_type>/<content_id>", methods=["GET", "POST"])
def modify_content(content_id, content_type):
    if request.method == "GET":
        if content_type == "post":
            post = posts.get_post(0, content_id)
            return render_template("edit.html", comment=None, post=post)
        elif content_type == "comment":
            comment = comments.get_comment(content_id)
            return render_template("edit.html", comment=comment, post=None)

    elif request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        authenticated_user = auth.user_id()
        method = request.form["method"]
        match (content_type, method):
            case "post", "put":
                title = request.form["title"]
                content = request.form["content"]
                if helpers.validate_length(title, "post_title") and helpers.validate_length(content, "post_content"):
                    if posts.update_post(content_id, content, title, authenticated_user):
                        flash("Post updated!")
                        return redirect("/edit/post/"+content_id)
                else:
                    flash("Maximum length of title or content exceeded.")

            case "post", "delete":
                if posts.delete_post(content_id, authenticated_user):
                    flash("Post deleted!")
                    return redirect("/users/"+str(authenticated_user))

            case "comment", "put":
                content = request.form["content"]
                if helpers.validate_length(content, "comment_content"):
                    if comments.update_comment(content_id, content, authenticated_user):
                        flash("Comment updated!")
                        return redirect("/edit/comment/"+content_id)
                else:
                    flash("Maximum length of title or content exceeded.")

            case "comment", "delete":
                if comments.delete_comment(content_id, authenticated_user):
                    flash("Comment deleted!")
                    return redirect("/users/"+str(authenticated_user))

# filter for timestamps

@app.template_filter('datetimeformat')
def datetime_format(value, format="%-d %b / %H:%M"):
    return value.strftime(format)

# error handlers

@app.errorhandler(401)
def forbidden():
    return render_template('error.html', code=401, err="Unauthorized – you do not have the rights to perform this action.")

@app.errorhandler(403)
def forbidden():
    return render_template('error.html', code=403, err="Forbidden – you do not have the rights to perform this action.")

@app.errorhandler(404)
def not_found():
    return render_template('error.html', code=404, err="This page does not exist :(")

@app.errorhandler(500)
def server_error():
    return render_template('error.html', code=500, err="An error occurred. Please try again.")

@app.errorhandler(Exception)
def exception_err(e):
    return render_template('error.html', code=500, err=repr(e))
