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


class users(Resource):
	'''
	get users data
	'''
	def get(self):
		'''
		get users public data
		'''
		data = request.args;
		user_id = data.get('user_id');
		if user_id:
			user = User.get_user_by_id(user_id=user_id);
			if user:
				return jsonify({'users':user.json()});
		users = [u.json() for u in User.get_all_users()];
		return jsonify({'users':users});


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
				return jsonify({
					'messege': f'new user {new_user.first_name} with id {new_user.id} added'
				})
	
		return jsonify({
			'error': 'user already exist or invalid inputs'
		});


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
					return jsonify({
					'messege': 'successfully authorized your token is now valid for 1h.',
					'access_token':token});
				else:
					return jsonify({'error': 'incorrect password or email'});
		return jsonify({'error': 'email or password missed.'});
	

class blogs(Resource):

	def get(self):
		author_id = request.args.get('author_id');
		blog_id = request.args.get('blog_id');
		blog_title = request.args.get('blog_title');

		if author_id or blog_id or blog_title:
			blogs = [bl.json() for bl in Blog.get_blog_by_user_id(
			author_id=author_id,
			blog_id=blog_id,
			blog_title=blog_title)];
		else:
			blogs = [blog.json() for blog in Blog.get_all_blogs()];
		return jsonify({'blogs':blogs});

	def post(self):

		# argument validator
		parser = reqparse.RequestParser();
		parser.add_argument('title', type=str, help='blog title');
		parser.add_argument('content', type=str, help='blog content');
		parser.add_argument('access_token', type=str, help='access token is required for authentcation');

		data = parser.parse_args();
		title = data.get('title');
		content = data.get('content');
		access_token = data.get('access_token');

		authorized_user = authorizer.isauthorized(access_token);
		if authorized_user:
			if title and content:
				New_blog = Blog.create_blog(title=title, content=content,author_id=authorized_user);
				return jsonify({'messege': f'new blog with id {New_blog.blog_id} created'});
		else:
			return jsonify({'error': 'unauthorized action'});

