from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app import mongo
from bson.objectid import ObjectId
from datetime import datetime

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/', methods=["GET", "POST"])
@login_required
def panel():
    post_id = request.args.get("edit")
    editing = None

    if post_id:
        editing = mongo.db.posts.find_one({"_id": ObjectId(post_id)})

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        description = content[:150] + '...' if len(content) > 150 else content
        pid = request.form.get("post_id")

        if pid:
            mongo.db.posts.update_one(
                {"_id": ObjectId(pid)},
                {"$set": {
                    "title": title,
                    "content": content,
                    "description": description,
                    "updated_at": datetime.utcnow()
                }}
            )
        else:
            mongo.db.posts.insert_one({
                "title": title,
                "content": content,
                "description": description,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "views": 0
            })

        return redirect(url_for('admin.panel'))

    posts = list(mongo.db.posts.find().sort("created_at", -1))
    return render_template("admin.html", posts=posts, editing=editing)

@bp.route('/delete/<post_id>')
@login_required
def delete_post(post_id):
    mongo.db.posts.delete_one({"_id": ObjectId(post_id)})
    return redirect(url_for('admin.panel')) 