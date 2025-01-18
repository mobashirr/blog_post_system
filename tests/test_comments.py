import unittest
import requests

BASE_URL = "http://localhost:5000/api"

class TestComments(unittest.TestCase):
    def setUp(self):
        self.auth_token = self.get_auth_token()

    def get_auth_token(self):
        payload = {"email": "test@test.com", "password": "password123"}
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)
        return response.json().get("token")

    def test_add_comment(self):
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        post_id = "some_existing_post_id"  # Replace with actual ID for testing
        payload = {"content": "This is a comment"}
        response = requests.post(f"{BASE_URL}/posts/{post_id}/comments", json=payload, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def test_get_comments(self):
        post_id = "some_existing_post_id"  # Replace with actual ID for testing
        response = requests.get(f"{BASE_URL}/posts/{post_id}/comments")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

if __name__ == "__main__":
    unittest.main()
