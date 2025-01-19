#!/usr/bin/ python3

'''
this module contain the api resources (endpoints logic)
'''

from flask import jsonify, request
from flask_restful import Resource
from application.models import Blog, User
from flask_restful import reqparse
from bcrypt import hashpw, gensalt, checkpw
from application.auth import AUTH as authorizer


def check_authorization():
	# get the access token from http headrs
	authoraization_header = request.headers.get("Authorization");
	if not authoraization_header:
		return jsonify({'error': 'missing the authrization header'}),401;
	if not authoraization_header.startswith("Bearer "):
		return jsonify({'error': 'Bearer Authization only allowed'}),401;
	access_token = authoraization_header.split()[1];
	authorized_user = authorizer.isauthorized(access_token);
	return authorized_user


class Users(Resource):
	'''
	we provide a resource for users private data (users emails and birthday, etc..)
	which requires an authentcation step also for updating or deleting an existing user
	'''
	def get(self):
		'''
		get users private data
		'''
		# authorization step:
		authorized_user = check_authorization();

		if authorized_user:
			# user is authrized and is accessing his own data
			user = User.get_user_by_id(user_id=authorized_user);
			if user:
				return {
					"status":"success",
					"message": "successfully authorized",
					'user': str(user.json_all_data())
				}, 200
		else:
			return {
					"status":"error",
					"message": "unauthorized user",
					'user':[]
				}, 401

	def put(self):
		'''
		update user data
		'''
		# authorization step:
		authorized_user = check_authorization()
		if authorized_user:
			data = request.get_json()
			if data:
				# Assuming the data contains keys like 'email', 'first_name', etc.
				update_result = User.update_user(authorized_user, data)
				return update_result
			else:
				return {
					"status":"error",
					'message': 'No new data provided'}, 400

		return {
			"status":"error",
			'message': 'Unauthorized'}, 401

	def delete(self):
		'''
		delete an existing user
		'''
		# authorization step:
		authorized_user = check_authorization();
		if authorized_user:
			user_to_delete = User.get_user_by_id(user_id=authorized_user)
			if user_to_delete:
				# delete all blogs related to this user:
				user_blogs = Blog.get_blog_by_user_id(author_id=user_to_delete.id)
				for blog in user_blogs:
					Blog.delete_blog(blog.blog_id)
				# delete the user
				result = User.delete_user(user_to_delete.id)
				return result
			else:
				return {
					"status":"error",
					"message": "user not found"
					},400
		return {
			"status":"error",
			'message': 'Unauthorized'}, 401


class UserList(Resource):
	'''
	get users data
	'''
	def get(self,user_id):
		'''
		get users public data
		'''
		if user_id:
			# non-zero id
			user = User.get_user_by_id(user_id=user_id);
			if not user:
				return {
					"status": "success",
					"message": "no user found",
					"user": []
				}, 204
			return {
				"status": "success",
				"message": "user found",
				"user": user.json()
			}, 200


		# when given id is zero then we want all users
		users = [u.json() for u in User.get_all_users()];
		return {
			"status": "success",
			"message": "list of all users provided",
			'users': users},200


class register(Resource):
	'''
		register endpoint logic
	'''
	def post(self):
		'''
			register a new user
		'''
		# arguments validator
		parser = reqparse.RequestParser();
		parser.add_argument('first_name', type=str, help='user first naem');
		parser.add_argument('last_name', type=str, help='user last name');
		parser.add_argument('email', type=str, help='user email');
		parser.add_argument('password', type=str, help='password');
		parser.add_argument('birthday', type=str, help='user first naem');	#

		data = parser.parse_args();
		first_name = data.get('first_name');
		last_name = data.get('last_name');
		email = data.get('email');
		password = data.get('password');
		birthday = data.get('birthday'); # not mandatory

		if first_name and last_name and email and password:
			user_exist = User.check_if_email_exist(email=email);
			if  not user_exist:
				'''create new user'''
				hashed_pass = hashpw(password.encode('utf-8'), gensalt());
				new_user = User.create_user(
					first_name=first_name,
					last_name=last_name,
					email=email,
					hashed_password=hashed_pass,
					birth_day=birthday);
				
				if new_user:
					return {
						"status":"success",
						'messege': 'new user registered successfully',
						'user':new_user.json()
					},201
				else:
					return { "status": "error", "message": "couldn't opreate this action right now." },503
			else:
				return {"status": "error", "message": "Email is already registered." },409
		else:
			return { "status":"error","message": "required data missing"},400


class login(Resource):
	'''
		login endpoint logic
	'''
	def post(self):
		'''
		log in new user
		'''
		# arguments validator
		parser = reqparse.RequestParser();
		parser.add_argument('email', type=str, help='user email');
		parser.add_argument('password', type=str, help='password');	
		data = parser.parse_args();
		email = data.get('email');
		password = data.get('password');

		if email and password:
			user_exist = User.check_if_email_exist(email=email);
			if user_exist:
				valid_pass = checkpw(password.encode('utf-8'),user_exist.hashed_password)

				if valid_pass:
					# start authintcation process:
					token = authorizer.authorize(user_exist);

					if token:
						return ({
						"status": "success",
						'message': 'successfully authorized your token is now valid for 2h.',
						'access_token':token}),200;
					else:
						return { "status": "error", "message": "couldn't opreate this action right now." },503
				else:
					return { "status":"error","message": "incorrect password or email"},400
		return { "status":"error","message": "required data missing"},400
	

class BlogsList(Resource):
	'''
	public blogs resource
	'''
	def get(self,blog_id):
		author_id = request.args.get('author_id');
		blog_title = request.args.get('blog_title');
		if blog_id or author_id or blog_title:
			blogs = [bl.json() for bl in Blog.get_blog_by_user_id(
			author_id=author_id,
			blog_id=blog_id,
			blog_title=blog_title)];
		else:
			blogs = [blog.json() for blog in Blog.get_all_blogs()];

		return {
			"status":"success",
			"message":"list of blogs provided",
			'blogs':blogs}, 200;


class Blogs(Resource):
	'''
	protected blogs resource
	'''
	def post(self):
		'''
		create new blog
		'''
		# Argument validator
		parser = reqparse.RequestParser()

		# authorization step:
		authorized_user = check_authorization();
		if authorized_user:
			parser.add_argument('title', type=str, help='Blog title')
			parser.add_argument('content', type=str, help='Blog content')
			data = parser.parse_args()
			title = data.get('title')
			content = data.get('content')
			if title and content:
				new_blog = Blog.create_blog(title=title, content=content, author_id=authorized_user)
				return new_blog, 201
			return {'message': 'Incomplete data received'}, 400
		else:
			return {'error': 'Unauthorized action'}, 401

	def put(self):
		'''
		update an existing blog
		'''
		# authorization step:
		authorized_user = check_authorization();

		if authorized_user:
			data = request.get_json()
			if data:
				blog_id = data.get('blog_id')
				blog_title = data.get('new_title')
				blog_content = data.get("new_content")
				new_data = {"title":blog_title,"content":blog_content}
				blog_to_update = Blog.get_blog_by_user_id(author_id=authorized_user,blog_id=blog_id).first()

				# we need to check if the user want to remove his own blog not someone else
				if blog_to_update:
					update_result = Blog.update_blog(blog_to_update.blog_id, new_data)
					return update_result
				else:
					return {'message': 'could not identify this blog as user blog'}, 400
			else:
				return {'message': 'No new data provided'}, 400

		return {'error': 'Unauthorized'}, 401

	def delete(self):
		'''
		delete an existing blog
		'''
		
		# Argument validator
		parser = reqparse.RequestParser()

		# authorization step:
		authorized_user = check_authorization();
		if authorized_user:
			parser.add_argument('blog_id', type=str, help='Blog title')
			parser.add_argument('blog_title', type=str, help='Blog content')
			data = parser.parse_args()
			blog_id = data.get('blog_id')
			blog_title = data.get('content')

			blog_to_delete = Blog.get_blog_by_user_id(author_id=authorized_user,blog_id=blog_id).first()

			if blog_to_delete:
				result = Blog.delete_blog(blog_to_delete.blog_id)
				return result
			else:
				return {"message": "blog not found"},400
		return {'error': 'Unauthorized'}, 401