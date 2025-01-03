#!/usr/bin/ python3

''' database models scheme '''


from application.utils import db
from datetime import datetime


# User Model
class User(db.Model):
    '''
    User table
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    birth_day = db.Column(db.Date, nullable=True)  # Optional field
    join_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def json(self):
        '''
        json representaion of the table
        '''
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

    def json_all_data(self):
        '''
        json representaion of the table
        '''
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'birthday': self.birth_day,
            'join_date': self.join_date
        };

    @staticmethod
    def create_user(first_name, last_name, email, hashed_password, birth_day=None):
        '''
        Create a new user record
        @first_name: user first name
        @last_name: user last name
        @email: user personal email
        @hashed_password: password hash (passwords shouldn't be stored directly)
        @birth_day: user birthday (defaults to '1990/01/01' if not provided)
        '''
        if not birth_day:
            birth_day = '1990/01/01'
        try:
            birth_day = datetime.strptime(birth_day, '%Y/%m/%d').date();
        except ValueError:
            print(f"Invalid date format for birth_day: {birth_day}. Please use YY/MM/DD format.")
            birth_day = datetime.strptime('1990/01/01', '%Y/%m/%d').date()

        new_user = User(first_name=first_name, last_name=last_name, email=email,
                        hashed_password=hashed_password, birth_day=birth_day)

        db.session.add(new_user)
        db.session.commit()

        return new_user

    @staticmethod
    def get_all_users():
        '''
        get all users in the database
        make sure this action won't be available for normal users
        '''
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        '''
        query user by id only
        '''
        return User.query.get(user_id)

    @staticmethod
    def check_if_email_exist(email):
        '''query user by email'''
        return User.query.filter_by(email=email).first()

    @staticmethod
    def update_user(user_id, updates):
        '''update user data'''
        user = User.query.get(user_id)
        if user:
            for key, value in updates.items():
                setattr(user, key, value)
            db.session.commit()
            return user
        return None

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False


# Blog Model
class Blog(db.Model):
    '''
    blogs table
    '''
    __tablename__ = 'blogs'
    blog_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_header_path = db.Column(db.String(100), default='default.png')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def json(self):
        user = User.get_user_by_id(self.author_id);
        if user:
            fullname = f'{user.first_name} {user.last_name}';
        else:
            fullname = 'unknown'
        return {
            'blog_id': self.blog_id,
            'title': self.title,
            'author_id': self.author_id,
            'author_name': fullname,
            'content': self.content,
            'image_header_path': self.image_header_path,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @staticmethod
    def create_blog(title, content, author_id=303, image_header_path='images/default.png'):
        new_blog = Blog(title=title,author_id=author_id, content=content, image_header_path=image_header_path)
        db.session.add(new_blog)
        db.session.commit()
        return new_blog

    @staticmethod
    def get_all_blogs():
        '''
        get list of all blogs instances
        '''
        return Blog.query.all()

    @staticmethod
    def get_blog_by_user_id(author_id=None,blog_id=None,blog_title=None):
        '''
            query blogs by author id or blog id or title
            @author_id: blog's author id
            @blog_id: blog id
            @blog_title: the blog title
            Return: list of blogs object
        '''
        query_dict = {}
        if author_id:
            query_dict['author_id'] = author_id;
        if blog_id:
            query_dict['blog_id'] = blog_id;
        if blog_title:
            query_dict['title'] = blog_title;
        return Blog.query.filter_by(**query_dict);

    @staticmethod
    def update_blog(blog_id, updates):
        blog = Blog.query.get(blog_id)
        if blog:
            for key, value in updates.items():
                setattr(blog, key, value)
            db.session.commit()
            return blog
        return None

    @staticmethod
    def delete_blog(blog_id):
        blog = Blog.query.get(blog_id)
        if blog:
            db.session.delete(blog)
            db.session.commit()
            return True
        return False


# Comment Model
class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.blog_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Convert to dictionary
    def json(self):
        return {
            'comment_id': self.comment_id,
            'author_id': self.author_id,
            'blog_id': self.blog_id,
            'content': self.content,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    # CRUD Operations
    @staticmethod
    def create_comment(author_id, blog_id, content):
        new_comment = Comment(author_id=author_id, blog_id=blog_id, content=content)
        db.session.add(new_comment)
        db.session.commit()
        return new_comment

    @staticmethod
    def get_all_comments():
        return Comment.query.all()

    @staticmethod
    def get_comment_by_id(comment_id):
        return Comment.query.get(comment_id)

    @staticmethod
    def update_comment(comment_id, updates):
        comment = Comment.query.get(comment_id)
        if comment:
            for key, value in updates.items():
                setattr(comment, key, value)
            db.session.commit()
            return comment
        return None

    @staticmethod
    def delete_comment(comment_id):
        comment = Comment.query.get(comment_id)
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return True
        return False


# ReadBlog Model
class ReadBlog(db.Model):
    __tablename__ = 'read_blogs'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.blog_id'), primary_key=True)
    read_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Convert to dictionary
    def json(self):
        return {
            'user_id': self.user_id,
            'blog_id': self.blog_id,
            'read_at': self.read_at
        }

    # CRUD Operations
    @staticmethod
    def create_read_blog(user_id, blog_id):
        new_read_blog = ReadBlog(user_id=user_id, blog_id=blog_id)
        db.session.add(new_read_blog)
        db.session.commit()
        return new_read_blog

    @staticmethod
    def get_all_read_blogs():
        return ReadBlog.query.all()

    @staticmethod
    def get_read_blog(user_id, blog_id):
        return ReadBlog.query.filter_by(user_id=user_id, blog_id=blog_id).first()

    @staticmethod
    def delete_read_blog(user_id, blog_id):
        read_blog = ReadBlog.query.filter_by(user_id=user_id, blog_id=blog_id).first()
        if read_blog:
            db.session.delete(read_blog)
            db.session.commit()
            return True
        return False
