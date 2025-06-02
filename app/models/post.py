from datetime import datetime
from bson.objectid import ObjectId

class Post:
    def __init__(self, title, content, author_id):
        self.title = title
        self.content = content
        self.author_id = author_id
        self.created_at = datetime.utcnow()

    @staticmethod
    def create_post(mongo, title, content, author_id):
        post = {
            'title': title,
            'content': content,
            'description': content[:150] + '...' if len(content) > 150 else content,
            'author_id': author_id,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        return mongo.db.posts.insert_one(post)
    
    @staticmethod
    def get_post(mongo, post_id):
        return mongo.db.posts.find_one({'_id': ObjectId(post_id)})
    
    @staticmethod
    def get_all_posts(mongo, limit=None, skip=0):
        cursor = mongo.db.posts.find().sort('created_at', -1).skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)
    
    @staticmethod
    def update_post(mongo, post_id, title, content):
        return mongo.db.posts.update_one(
            {'_id': ObjectId(post_id)},
            {
                '$set': {
                    'title': title,
                    'content': content,
                    'description': content[:150] + '...' if len(content) > 150 else content,
                    'updated_at': datetime.utcnow()
                }
            }
        )
    
    @staticmethod
    def delete_post(mongo, post_id):
        return mongo.db.posts.delete_one({'_id': ObjectId(post_id)})

    @staticmethod
    def get_by_id(post_id):
        return mongo.db.posts.find_one({"_id": ObjectId(post_id)})

    def save(self):
        return mongo.db.posts.insert_one(self.__dict__) 