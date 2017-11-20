from flask import Flask, jsonify, abort, make_response
from flask import request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/demo?charset=utf8'

db = SQLAlchemy(app)

class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    content = db.Column(db.Text)

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return '<Articles %r>' % self.title

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@app.route('/blog/api/articles', methods=['GET', 'POST'])
def get_articles():
    if request.method == "GET":
        articles = json.dumps([article.as_dict()
                               for article in Articles.query.all()])
        return jsonify({'articles': articles})

    elif request.method == "POST":
        if not request.json or not 'title' in request.json:
            abort(404)
        try:
            article = Articles(title=request.json[
                               'title'], content=request.json.get('content', ''))
            db.session.add(article)
            db.session.commit()
            articles = json.dumps([article.as_dict()
                                   for article in Articles.query.all()])
            return jsonify({'articles': articles}), 201
        except Exception as e:
            return jsonify({'result': False, 'message': str(e)})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001, debug=True)