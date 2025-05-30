from flask import Blueprint, render_template, current_app
from app import mongo
from app.models.post import Post
from datetime import datetime
from bson.objectid import ObjectId

bp = Blueprint('blog', __name__, url_prefix='/blog')

def estimate_read_time(content):
    words_per_minute = 200
    word_count = len(content.split())
    return max(1, round(word_count / words_per_minute))

def format_date_ru(date):
    months_ru = {
        1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
        5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
        9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
    }
    return f"{date.day} {months_ru[date.month]} {date.year}"

@bp.route('/')
def index():
    posts = Post.get_all_posts(mongo)
    for post in posts:
        post['read_time'] = estimate_read_time(post.get('content', ''))
        post['formatted_date'] = format_date_ru(post['created_at'])
        post['id'] = str(post['_id'])
        post['views'] = post.get('views', 0)  # Add view counter
    return render_template('blog.html', posts=posts)

@bp.route('/<post_id>')
def view_post(post_id):
    try:
        # Increment view counter first
        mongo.db.posts.update_one(
            {'_id': ObjectId(post_id)},
            {'$inc': {'views': 1}}
        )
        
        # Then get the updated post
        post = Post.get_post(mongo, post_id)
        if post:
            post['read_time'] = estimate_read_time(post.get('content', ''))
            post['formatted_date'] = format_date_ru(post['created_at'])
            post['views'] = post.get('views', 0)
            return render_template('post.html', post=post)
    except Exception as e:
        current_app.logger.error(f"Error viewing post {post_id}: {str(e)}")
    return render_template('404.html'), 404 