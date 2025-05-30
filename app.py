from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_wtf.csrf import CSRFProtect
from bson.objectid import ObjectId
from datetime import datetime
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app)

mongo = PyMongo(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# remake
class Admin(UserMixin):
    def __init__(self, id):
        self.id =   id

@login_manager.user_loader
def load_user(user_id):
    if user_id == "admin":
        return Admin("admin")
    return None

@app.route("/")
def index():
    return render_template("index.html")

def estimate_read_time(content):
    words_per_minute = 200
    word_count = len(content.split())
    minutes = max(1, round(word_count / words_per_minute))
    return minutes

# Список постов
@app.route("/blog")
def blog():
    posts = list(mongo.db.posts.find().sort("created_at", -1))
    for post in posts:
        post['read_time'] = estimate_read_time(post.get('content', ''))
        post['formatted_date'] = post['created_at'].strftime('%b %d, %Y')
        post['id'] = str(post['_id'])
    return render_template("blog.html", posts=posts)

# Просмотр поста
@app.route("/blog/<post_id>")
def show_post(post_id):
    
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    return render_template("post.html", post=post)

# Авторизация
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            if request.form["username"] == "admin" and request.form["password"] == "123": #REMAKE
                login_user(Admin("admin"))
                return redirect(url_for("admin.panel"))
            else:
                flash('Неверный логин или пароль', 'error')
        except Exception as e:
            app.logger.error(f"Login error: {str(e)}")
            flash('Произошла ошибка при входе', 'error')
    return render_template("login.html")

# Выход
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

# Админка
@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin_panel():
    post_id = request.args.get("edit")
    editing = None

    if post_id:
        editing = mongo.db.posts.find_one({"_id": ObjectId(post_id)})

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        description = content[:150]
        pid = request.form.get("post_id")

        if pid:
            mongo.db.posts.update_one(
                {"_id": ObjectId(pid)},
                {"$set": {"title": title, "content": content, "description": description}}
            )
        else:
            mongo.db.posts.insert_one({
                "title": title,
                "content": content,
                "description": description,
                "created_at": datetime.utcnow()
            })

        return redirect(url_for("admin_panel"))

    posts = list(mongo.db.posts.find().sort("created_at", -1))
    return render_template("admin.html", posts=posts, editing=editing)

# Удаление поста
@app.route("/delete/<post_id>")
@login_required
def delete_post(post_id):
    mongo.db.posts.delete_one({"_id": ObjectId(post_id)})
    return redirect(url_for("admin_panel"))

@app.route('/contact')
def contact():
    return render_template('contact.html')

# blueprints
from app.routes import blog, admin
app.register_blueprint(blog.bp)
app.register_blueprint(admin.bp)

if __name__ == "__main__":
    app.run()
