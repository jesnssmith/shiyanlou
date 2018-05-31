# import json
from flask_sqlalchemy import SQLAlchemy 
from flask import Flask,render_template,redirect,abort
import os
import re
from datetime import datetime
from pymongo import MongoClient

app=Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root@localhost/shiyanlou'
db=SQLAlchemy(app)
client=MongoClient('127.0.0.1',27017)
db_mongo=client.shiyanlou.tags


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category= db.relationship('Category', backref=db.backref('file', lazy='dynamic'))
    content = db.Column(db.Text)
    
    def __init__(self,title,created_time,category,content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    def add_tag(self, tag_name):
        doc = db_mongo.find_one({'id': self.id})
        if doc:
            tags = doc['tags']
            if tag_name not in tags:
                tags.append(tag_name)
                db_mongo.update_one({'id': self.id}, {'$set': {'tags': tags}})
        else:
            db_mongo.insert_one({'id': self.id, 'tags': [tag_name]})

    def remove_tag(self, tag_name):
        doc = db_mongo.find_one({'id': self.id})
        if doc:
            tags = doc['tags']
            if tag_name in tags:
                tags.remove(tag_name)
                db_mongo.update_one({'id': self.id}, {'$set': {'tags': tags}})

    @property
    def tags(self):
        return db_mongo.find_one({"id":self.id})['tags']

    def __repr__(self):
        return '<File %r>' %self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return "<Category %r>" %self.name




# def get_json():
#       result={}
#       file_list=os.listdir('/home/shiyanlou/files/')
#       for file in file_list:
#               with open(os.path.join('/home/shiyanlou/files/',file)) as f:
#                       result[file.split('.')[0]]=json.loads(f.read())
#       return result

# files=get_json()
# for value in files.values():
#       re.sub(r'\*n','',value['content'])




@app.route('/')
def index():
    files=File.query.all()
    
    
    return render_template('index.html',files = files)

@app.route('/files/<file_id>')
def file(file_id):
    file=File.query.filter_by(id=file_id).first()
    if not file:
            abort(404)
    return render_template('file.html', file=file)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404


def create_db():
    db.create_all()
    java=Category('Java')
    python =  Category('Python')
    file1 = File('Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
    file2 = File('Hello Python', datetime.utcnow(),python,'File Content - Python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()
    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('tech')
    file2.add_tag('python')

if __name__ == "__main__":
    create_db()
