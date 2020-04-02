# from flask import Flask, g, request
# from couchdb.design import ViewDefinition
# from flaskext.couchdb import CouchDBManager
# from flaskext.couchdb import Document, TextField, FloatField, DictField, Mapping,ListField, IntegerField
#
#
#
# app = Flask(__name__)
#
# app.config.update(
#     COUCHDB_SERVER='http://admin:123@localhost:5984',
#     COUCHDB_DATABASE='graphaitedb'
# )
#
# manager = CouchDBManager()
# manager.setup(app)
#
#
# class BlogPost(Document):
#     doc_type = 'blogpost'
#
#     title = TextField()
#     content = TextField()
#     author = TextField()
#
#
#
# """
# Add doc
# """
# @app.route("/add", methods=['GET'])
# def add():
#     post = BlogPost(title='Hello', content='Hello, world!', author='Steve')
#     post.id = 'tesid2'
#     post.store()
#
#     return "OK"
#
# """
# Flask main
# """
# if __name__ == "__main__":
#     #socketio.run(app)
#     app.debug = True
#     app.run("0.0.0.0")