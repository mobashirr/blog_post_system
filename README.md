# blog_post_system


# about the project
this project is a simple back-end system for blog posts web based application
providing a simple api at ... ip ...


# getting started

- first clone this repo
```
git clone 
```

- install project requirments (up to you if you use venv)
```
pip3 install -r requirements.txt
```

- you may need to configure you own database and redis client server


#  key features
- authintcation system implemented with session mannger (using redis)
- CRUD opreations on blogs (create, delete, ..etc)
- posts storage

# project architicure
```
/blog_post_system
    /application
        __init__.py     # application initialization
        resources.py    # api resources declaration
        models.py       # database models
        auth.py         # authentication system
        /utils
            __init__.py
            redis_client.py     # redis client used for session mangement
            database.py  # the database client used to intract with our db
    app.py  # app entry point
```


# api endpoints

1. Get requests

- users

sence its a blog post system some data will be in public,
things like posts and post's author name or post's comments, etc.. 
but it has to be limited to the need only
meaning we can't publish sensetive data(passwords, email, phone number, etc..)

this endpoint is for public data encluding first name, last name and uniuqe id only so there is no authentcaion needed
```
api/v1/users/<int:user_id>
```
example usage:
```
curl -X GET "http://127.0.0.1:5000/api/v1/users/2"
```
note: if you set user_id to zero you get list of all users

to get user personal data use this endpoint which need the authentcation step
each user can have access to his own private data only
```
api/v1/users
```
example usage:
```
curl -X GET "http://127.0.0.1:5000/api/v1/users" \
-H "Authorization: Bearer <access_token>"
```
you should get response like this
```
{
  "users": {
    "birthday": "Mon, 01 Jan 1990 00:00:00 GMT",
    "email": "something@gmail.com",
    "first_name": "someone",
    "id": 4,
    "join_date": "Tue, 31 Dec 2024 17:56:46 GMT",
    "last_name": "bin someone",
    ...
  }
}
```

- blogs

```
/api/v1/blogs
```
you can search for blogs by author_id or blog_id or even blog_title
by adding this filters in the query parameters or the url of the request,
by default if no parameters given all posts will be returned (soon we will implement pageintaion)
```
curl -X GET "http://127.0.0.1:5000/api/v1/blogs?author_id=303&blog_id=4&blog_title=blog%20title"
```
response will be like this:
```
{
  "blogs": [
    {
      "author_id": 303,
      "author_name": "someone",
      "blog_id": 4,
      "content": "blog contant",
      "created_at": "Tue, 31 Dec 2024 12:13:57 GMT",
      "image_header_path": "default.png",
      "title": "blog title",
      "updated_at": "Tue, 31 Dec 2024 12:13:57 GMT",
      ...
    }
  ]
}
```

2. Post requests

- register a new user
```
/api/v1/register
```
example usage:
```
curl -X POST -H "Content-Type: application/json" -d '{"first_name": "someone","last_name": "bin fulan", "email": "some@gmail.com", "password": "anypass", "birthday": "2020/04/16"}' http://127.0.0.1:5000/api/v1/register
```
note: birthday is default to 1990/1/1 if not submited

- login (get authorization key)
```
/api/v1/login
```
```
curl -X POST -H "Content-Type: application/json" -d '{"email": "some@gmail.com", "password": "anypass"}' http://127.0.0.1:5000/api/v1/login
```
you should get response like this:
```
{
  "access_token": <"29999331e13108d00dbae7584b1c2e113253af44e16b7be013e7a04544722a91">,
  "messege": "successfully authorized, your token is valid for 2h."
}
```

- post new blog
```
api/v1/blogs
```
example usage:
```
curl -X POSt \
-H "Authorization: Bearer <access_token>" \
-H "Content-Type: application/json" \
-d '{"title": "blog title","content": "blog contnt"}' \
http://127.0.0.1:5000/api/v1/blogs
```

3. put reqests

```
api/v1/users
```
example usage:
```
curl -X PUT \
-H "Authorization: Bearer  <acess_token>" \
-H "Content-Type: application/json" \
-d '{"email": "new@gmail.com","first_name": "new first name", "password": "newpass"}' \
http://127.0.0.1:5000/api/v1/users

```
you can modify: ['first_name', 'last_name', 'email', 'birthday', "password"]

you may get response like this :
```
{
    "message": "User 6 updated successfully",
    "user": {
        "id": 6,
        "first_name": "new AA first name",
        "last_name": "new BB last_name"
    }
}
```
or
```
{
    "error": "Email new@gmail.com is already in use."
}
```