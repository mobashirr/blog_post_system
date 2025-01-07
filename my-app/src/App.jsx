import { useState, useEffect } from 'react';
import AuthForm from './components/AuthForm';
import BlogList from './components/BlogList';
import BlogForm from './components/BlogForm';

const App = () => {
  const [user, setUser] = useState(null);
  const [blogs, setBlogs] = useState([]);
  const [editingBlog, setEditingBlog] = useState(null);
  const [isLogin, setIsLogin] = useState(true);

  useEffect(() => {
    // Check for stored token and fetch user data if exists
    const token = localStorage.getItem('token');
    if (token) {
      fetchUserData(token);
    }
  }, []);

  useEffect(() => {
    if (user) {
      fetchBlogs();
    }
  }, [user]);

  const fetchUserData = async (token) => {
    try {
      // Add your API call here to validate token and get user data
      // setUser(userData);
    } catch (error) {
      console.error('Error fetching user data:', error);
      localStorage.removeItem('token');
    }
  };

  const fetchBlogs = async () => {
    try {
      // Add your API call here to fetch blogs
      // setBlogs(blogsData);
    } catch (error) {
      console.error('Error fetching blogs:', error);
    }
  };

  const handleAuth = async (formData) => {
    try {
      // Add your API call here for login/register
      // const response = await api.post('/auth/login', formData);
      // localStorage.setItem('token', response.data.token);
      // setUser(response.data.user);
    } catch (error) {
      console.error('Auth error:', error);
    }
  };

  const handleCreateBlog = async (formData) => {
    try {
      // Add your API call here to create blog
      // const response = await api.post('/blogs', formData);
      // setBlogs([...blogs, response.data]);
    } catch (error) {
      console.error('Error creating blog:', error);
    }
  };

  const handleUpdateBlog = async (formData) => {
    try {
      // Add your API call here to update blog
      // const response = await api.put(`/blogs/${editingBlog.id}`, formData);
      // setBlogs(blogs.map(blog => blog.id === editingBlog.id ? response.data : blog));
      setEditingBlog(null);
    } catch (error) {
      console.error('Error updating blog:', error);
    }
  };

  const handleDeleteBlog = async (blogId) => {
    try {
      // Add your API call here to delete blog
      // await api.delete(`/blogs/${blogId}`);
      // setBlogs(blogs.filter(blog => blog.id !== blogId));
    } catch (error) {
      console.error('Error deleting blog:', error);
    }
  };

  if (!user) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-center mb-4">
          <button
            onClick={() => setIsLogin(!isLogin)}
            className="text-blue-500 hover:text-blue-600"
          >
            Switch to {isLogin ? 'Register' : 'Login'}
          </button>
        </div>
        <AuthForm isLogin={isLogin} onSubmit={handleAuth} />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Blog Dashboard</h1>
        <button
          onClick={() => {
            localStorage.removeItem('token');
            setUser(null);
          }}
          className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
        >
          Logout
        </button>
      </div>
      <BlogForm
        blog={editingBlog}
        onSubmit={editingBlog ? handleUpdateBlog : handleCreateBlog}
      />
      <div className="mt-8">
        <BlogList
          blogs={blogs}
          onEdit={setEditingBlog}
          onDelete={handleDeleteBlog}
        />
      </div>
    </div>
  );
};

export default App;