# blog_post_system


# about the project
this project is a simple back-end system for blog posts web based application
providing a simple api at ... ip ...

# key features
- authintcation system implemented with session mannger
- CRUD opreations on blogs (create, delete, update, ..etc)
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
            database_client.py  # the database client used to intract with our db
    app.py  # app entry point
```


# api endpoints

1. Get requests

- get all blogs
    ```
    /api/v1/blogs/
    ```
- get blogs by user id
        ```
            /api/v1/blogs/<int:num>
       ```

2. Post requests
    -- post new user
        /api/users {name,age,email}
    -- post new blog
        ```
            api/blog/ {title,content}
        ```
    -- register a new user

3. put requests

- alter user data
    ```
        api/users/ {new data}
    ```
- alter blogs data
    ```
        api/blogs/ {new data}
    ```
4. Delete requests
-
-
-

