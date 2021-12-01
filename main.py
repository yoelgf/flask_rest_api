from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
db.create_all()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50))
    author = db.Column(db.String(50))
    title = db.Column(db.String(50))
    description = db.Column(db.String(200))
    url = db.Column(db.String(50))
    urlToImage = db.Column(db.String(50))
    publishedAt = db.Column(db.String(50))
    content = db.Column(db.String(255))
    category = db.Column(db.String(50))

    def __repr__(self):
        return '<Post %s>' % self.title


class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "source","author","title","description","url","urlToImage","publishedAt", "content","category")


post_schema = PostSchema()
posts_schema = PostSchema(many=True)


class PostListResource(Resource):
    def get(self):
        posts = Post.query.all()
        return posts_schema.dump(posts)

    def post(self):
        new_post = Post(
         source=request.json['source'],
         author=request.json['author'],
         title=request.json['title'],
         description=request.json['description'],
         url=request.json['url'],
         urlToImage=request.json['urlToImage'],
         publishedAt=request.json['publishedAt'],
         content=request.json['content'],
         category=request.json['category']
        )
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post)


class PostResource(Resource):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post_schema.dump(post)

    def patch(self, post_id):
        post = Post.query.get_or_404(post_id)

        if 'source' in request.json:
            post.source = request.json['source']
        if 'author' in request.json:
            post.author = request.json['author']
        if 'title' in request.json:
            post.title = request.json['title']
        if 'description' in request.json:
            post.description = request.json['description']
        if 'url' in request.json:
            post.url = request.json['url']
        if 'urlToImage' in request.json:
            post.urlToImage = request.json['urlToImage']
        if 'publishedAt' in request.json:
            post.publishedAt = request.json['publishedAt']
        if 'content' in request.json:
            post.content = request.json['content']
        if 'category' in request.json:
            post.category = request.json['category']

        db.session.commit()
        return post_schema.dump(post)

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204


api.add_resource(PostListResource, '/posts')
api.add_resource(PostResource, '/posts/<int:post_id>')


if __name__ == '__main__':
    app.run(debug=True)