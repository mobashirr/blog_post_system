
# Blog Post System API

## About the Project
This project is a simple back-end system API for a blog post web-based application. A live API Demo is hosted at:
**http://157.245.135.17:7777/api/v1**

---

## Getting Started

1- Clone the repository:
   ```bash
   git clone
   ```

2- Install project requirements:
   ```bash
   pip3 install -r requirements.txt
   ```
   *(Optional: Use a virtual environment for dependency management)*

3- Configure your database and Redis client server as needed.

---

## Key Features
- **Authentication System**: Implemented using session management (Redis).
- **CRUD Operations**: Create, read, update, and delete blog posts.
- **Post Storage**: Manage and store user posts efficiently.

---

## Project Architecture
```
/blog_post_system
    /application
        __init__.py       # Application initialization
        resources.py      # API resources declaration
        models.py         # Database models
        auth.py           # Authentication system
        /utils
            __init__.py
            redis_client.py  # Redis client for session management
            database.py      # Database client for database interactions
    app.py  # Application entry point
```

---

## API Endpoints

### **1. GET Requests**

#### **Users**
- **Public User Data**
  Endpoint: `api/v1/users/<int:user_id>`
  - Provides public user data which is first name, last name, and unique ID only.
  - No authentication required.
  - Example:
    ```bash
    curl -X GET "http://127.0.0.1:5000/api/v1/users/2"
    ```
  - Note: Use `user_id=0` to retrieve a list of all users.

- **Private User Data**
  Endpoint: `api/v1/users`
  - Retrieves a user's private data. Authentication required.
  - Example:
    ```bash
    curl -X GET "http://127.0.0.1:5000/api/v1/users"     -H "Authorization: Bearer <access_token>"
    ```
  - Responses:
    ```json
    {
      "status": "success",
      "message": "successfully authorized",
      "user":
      {
        "id": 13,
        "first_name": "some",
        "last_name": "one",
        "email": "someone@gmail.com",
        "birthday": "2009-05-23",
        "join_date": "2025-01-07 20:26:52"
      }
    ```

#### **Blogs**
- Endpoint: `/api/v1/blogs/<int:blog_id>?author_id=<int:id>&blog_title=<str:title>`
  - Retrieves blogs based on optional filters like `author_id`, `blog_id`, or `blog_title`.
  - Example:
    ```bash
    curl -X GET "http://127.0.0.1:5000/api/v1/blogs/4?author_id=303&blog_title=blog%20title"
    ```
  - Response:
    ```json
    {
      "status": "success",
      "message": "list of all blogs provided",
      "blogs": [
        {
          "author_id": 303,
          "author_name": "John Doe",
          "blog_id": 4,
          "content": "Blog content",
          "created_at": "Tue, 31 Dec 2024 12:13:57 GMT",
          "image_header_path": "default.png",
          "title": "Blog Title",
          "updated_at": "Tue, 31 Dec 2024 12:13:57 GMT"
        }
      ]
    }
    ```

### **2. POST Requests**

#### **Register a New User**
- Endpoint: `/api/v1/register`
  - Example:
    ```bash
    curl -X POST -H "Content-Type: application/json"     -d '{"first_name": "Jane", "last_name": "Doe", "email": "jane@gmail.com", "password": "password", "birthday": "1990/01/01"}'     http://127.0.0.1:5000/api/v1/register
    ```

#### **User Login (Authorization)**
- Endpoint: `/api/v1/login`
  - Example:
    ```bash
    curl -X POST -H "Content-Type: application/json"     -d '{"email": "jane@gmail.com", "password": "password"}'     http://127.0.0.1:5000/api/v1/login
    ```
  - Response:
    ```json
    {
      "status": "success",
      "access_token": "<token>",
      "message": "Successfully authorized. Your token is valid for 2 hours."
    }
    ```

#### **Create a New Blog**
- Endpoint: `/api/v1/blogs`
  - Example:
    ```bash
    curl -X POST     -H "Authorization: Bearer <access_token>"     -H "Content-Type: application/json"     -d '{"title": "Blog Title", "content": "Blog Content"}'     http://127.0.0.1:5000/api/v1/blogs
    ```
      - Response:
    ```json
    {
      "status": "success",
      "message": "new blog with id 13 created"
      "blog":
      {
        "blog_id": 13,
        "title": "title",
        "author_id": 13,
        "author_name": "name",
        "content": "content",
        "created_at": "2025-01-07 20:36:03",
        "updated_at": "2025-01-07 20:36:03"
      }
    }
    ```

### **3. PUT Requests**

#### **Update User Information**
- Endpoint: `/api/v1/users`
  - Example:
    ```bash
    curl -X PUT     -H "Authorization: Bearer <access_token>"     -H "Content-Type: application/json"     -d '{"email": "new_email@gmail.com", "first_name": "New Name", "password": "newpassword"}'     http://127.0.0.1:5000/api/v1/users
    ```

#### **Update Blog Information**
- Endpoint: `/api/v1/blogs`
  - Example:
    ```bash
    curl -X PUT     -H "Authorization: Bearer <access_token>"     -H "Content-Type: application/json"     -d '{"blog_id": 4, "new_title": "Updated Title", "new_content": "Updated Content"}'     http://127.0.0.1:5000/api/v1/blogs
    ```
  - Response:
    ```json
    {
      "status": "success",
      "message": "Blog 4 updated successfully",
      "blog": {
        "blog_id": 4,
        "title": "Updated Title",
        "content": "Updated Content",
        "author_name": "John Doe",
        "created_at": "2025-01-05 17:28:28",
        "updated_at": "2025-01-05 17:28:29"
      }
    }
    ```

### **4. DELETE Requests**

#### **Delete a User**
- Endpoint: `/api/v1/users`
  - Example:
    ```bash
    curl -X DELETE     -H "Authorization: Bearer <access_token>"     -H "Content-Type: application/json"     http://127.0.0.1:5000/api/v1/users
    ```
  - Response:
    ```json
    {
      "status": "success",
      "message": "user have been deleted",
      "user": 
      {
        "id": 13,
        "first_name": "new name",
        "last_name": "new last name"
      }
    }
    ```

#### **Delete a Blog**
- Endpoint: `/api/v1/blogs`
  - Example:
    ```bash
    curl -X DELETE     -H "Authorization: Bearer <access_token>"     -H "Content-Type: application/json"     -d '{"blog_id": 4}'     http://127.0.0.1:5000/api/v1/blogs
    ```
  - Response:
    ```json
    {
      "message": "blog have been deleted",
      "blog": {
        "blog_id": 4,
        "title": "Title",
        "author_name": "John Doe"
      }
    }
    ```
