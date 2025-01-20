import unittest
import requests

BASE_URL = "http://localhost:5000/api"
#testing posts
class TestPosts(unittest.TestCase):
    def setUp(self):
        # Register and log in to get the auth token
        self.auth_token = self.get_auth_token()

    def get_auth_token(self):
        payload = {"email": "test@test.com", "password": "password123"}
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)
        return response.json().get("token")

    def test_create_post(self):
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        payload = {"title": "Test Post", "content": "This is a test post"}
        response = requests.post(f"{BASE_URL}/posts", json=payload, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def test_get_all_posts(self):
        response = requests.get(f"{BASE_URL}/posts")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_update_post(self):
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        post_id = "some_existing_post_id"  # Replace with actual ID for testing
        payload = {"title": "Updated Title", "content": "Updated content"}
        response = requests.put(f"{BASE_URL}/posts/{post_id}", json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        post_id = "some_existing_post_id"  # Replace with actual ID for testing
        response = requests.delete(f"{BASE_URL}/posts/{post_id}", headers=headers)
        self.assertEqual(response.status_code, 204)

if __name__ == "__main__":
    unittest.main()
