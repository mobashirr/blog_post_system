import unittest
import requests

BASE_URL = "http://localhost:5000/api"

#testing authentication
class TestAuthentication(unittest.TestCase):
    def test_register_user(self):
        payload = {"username": "testuser", "email": "test@test.com", "password": "password123"}
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("token", response.json())

    def test_login_user(self):
        payload = {"email": "test@test.com", "password": "password123"}
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_invalid_login(self):
        payload = {"email": "invalid@test.com", "password": "wrongpassword"}
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", response.json())

if __name__ == "__main__":
    unittest.main()
