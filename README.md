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

- blogs
```
/api/v1/blogs
```
to access this endpoint include the access token
in the http headers under -H "Authorization: Bearer <access_token>.

you can search for blogs by author_id or blog_id or even blog_title
by adding this filters in the query parameters or the url of the request
```
curl -X GET "http://127.0.0.1:5000/api/v1/blogs?author_id=1&blog_id=1&blog_title=My%20First%20Blog" \
-H "Authorization: Bearer <access_token>"
```

2. Post requests

- register a new user
```
/api/v1/register
```
example usage:
```
curl -X POST -H "Content-Type: application/json" -d '{"first_name": "someone","last_name": "bin fulan", "email": "something@gmail.com", "password": "anypass", "birthday": "2020/04/16"}' http://127.0.0.1:5000/api/v1/register
```
note: birthday is default to 1990/1/1 if not submited

- login (get authorization key)
```
/api/v1/login
```
```
curl -X POST -H "Content-Type: application/json" -d '{"first_name": "someone","last_name": "bin fulan", "email": "something@gmail.com", "password": "anypass"}' http://127.0.0.1:5000/api/v1/login
```
you should get response like this:
```
{
  "access_token": "8602e158abc2089561159e42348aa869c645ee6f198a04b5f6a678cc3150c256",
  "messege": "successfully authorized, your token is valid for 2h."
}
```

- post new blog
```
api/v1/blogs
```
example usage:
```
curl -X POST -H "Content-Type: application/json" -d '{"title": "blog title","content": "blog contant", "access_token": "8602e158abc2089561159e42348aa869c645ee6f198a04b5f6a678cc3150c256"}' http://127.0.0.1:5000/api/v1/blogs
```