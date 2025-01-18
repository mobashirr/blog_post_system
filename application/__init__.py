#!/usr/bin/ python3

'''
intialaization of the application instances
this is python packege only import the name of
the dir and this file will be imported
'''


from flask import Flask
from flask_restful import Api
from application.utils import db

# creating flask app and flask_rest extention
app = Flask(__name__)
api = Api(app)

# app config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' # we are using flask sqlachemy ORM
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()  # Ensures database tables are created


# add the resources to flask application
from application.resources import BlogsList, Blogs, register, login, UserList, Users
api.add_resource(BlogsList, '/api/v1/blogs/<int:blog_id>');
api.add_resource(Blogs, '/api/v1/blogs');
api.add_resource(register, '/api/v1/register');
api.add_resource(login, '/api/v1/login');
api.add_resource(UserList, '/api/v1/users/<int:user_id>');   # public users list
api.add_resource(Users, '/api/v1/users'); # private users resource
