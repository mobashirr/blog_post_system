import unittest
from application import app

#testing overall respoones in the project
class TestUserEndpoints(unittest.TestCase):
	def setUp(self):
		self.tester = app.test_client()

	def test_get_all_users(self):
		response = self.tester.get('api/v1/users/0')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content_type, 'application/json')
		self.assertEqual(response.json.get('status'), 'success')

	def test_get_user_by_id(self):
		user_id = 2
		response = self.tester.get(f'api/v1/users/{user_id}')
		self.assertEqual(response.status_code, 200)
		data = response.json
		self.assertEqual(data.get('status'), 'success')
		self.assertEqual(data['user']['id'], user_id)

	def test_get_nonexistent_user(self):
		response = self.tester.get('api/v1/users/9999999')
		self.assertEqual(response.status_code, 204)

class TestBlogEndpoints(unittest.TestCase):
	def setUp(self):
		self.tester = app.test_client()

	def test_get_all_blogs(self):
		response = self.tester.get('api/v1/blogs/0')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content_type, 'application/json')
		self.assertEqual(response.json.get('status'), 'success')

	def test_get_blog_by_id(self):
		blog_id = 1
		response = self.tester.get(f'api/v1/blogs/{blog_id}')
		self.assertEqual(response.status_code, 200)
		data = response.json
		self.assertEqual(data.get('status'), 'success')
		self.assertEqual(data['blogs'][0]['blog_id'], blog_id)

class TestUserActions(unittest.TestCase):
	def setUp(self):
		self.tester = app.test_client()
		self.test_user = {
			"first_name": "Test",
			"last_name": "User",
			"email": "testuser@example.com",
			"password": "testpassword",
			"birthday": "1990/1/1"
		}
		self.test_user2 = {
			"first_name": "Test",
			"last_name": "User",
			"email": "testuserdub@example.com",
			"password": "testpassword",
			"birthday": "1990/1/1"
		}
		self.test_user_missning_data = {
			"first_name": "Test",
			"last_name": "User",
			"password": "testpassword",
			"birthday": "1990/1/1"
		}

	def test_register_user(self):
		response = self.tester.post('/api/v1/register', json=self.test_user)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.json['status'], 'success')

	def test_register_user_invalid_input(self):
		# missing email or password:
		response = self.tester.post('/api/v1/register', json=self.test_user_missning_data)
		self.assertEqual(response.status_code, 400, "we should get 400 cause required data are missed")
		self.assertEqual(response.json['status'], 'error')

	def test_register_user_exist(self):
		''' user already exist case '''
		# register the user
		response = self.tester.post('/api/v1/register', json=self.test_user2)
		self.assertEqual(response.status_code, 201,)
		self.assertEqual(response.json['status'], 'success')
		# try to regisrer again:
		response = self.tester.post('/api/v1/register', json=self.test_user2)
		self.assertEqual(response.status_code, 409, "dublcated user is forbiden")
		self.assertEqual(response.json['status'], 'error')

	def test_login_user(self):
		# Ensure user exists before login attempt
		self.tester.post('/api/v1/register', json=self.test_user)

		# try to login:
		response = self.tester.post('/api/v1/login', json={
			"email": self.test_user['email'],
			"password": self.test_user['password']
		})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json['status'], 'success')
		self.assertIn('access_token', response.json)

	def test_update_user(self):
		'''
		update an existing user info
		'''
		# Ensure user exists before update attempt
		self.tester.post('/api/v1/register', json=self.test_user)
		response = self.tester.post('/api/v1/login', json={
			"email": self.test_user['email'],
			"password": self.test_user['password']
		})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json['status'], 'success')
		self.assertIn('access_token', response.json)
		access_token = response.json['access_token']

		# update user info
		new_data = {
			"first_name": "new first name",
			"last_name": "new last name",
			"email": "new_email_4000@gmail.com",
			"password": "new pass",
			"birthday": "2008/5/3"
		}
		response = self.tester.put(
			'api/v1/users',
			headers={"Authorization": f"Bearer {access_token}"},
			json=new_data
			)
		print(type(response.json))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json['status'], 'success')
		
		# check if the data have changed:

		# first login with the new data
		response = self.tester.post('/api/v1/login', json={
			"email": new_data['email'],
			"password": new_data['password']
		})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json['status'], 'success', "we should be able to login with the new data")
		self.assertIn('access_token', response.json)
		access_token = response.json['access_token']

		# get the user data to validate changes
		response = self.tester.get(
			'api/v1/users',
			headers={"Authorization": f"Bearer {access_token}"}
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json['status'], 'success')
		self.assertIn('user', response.json)

		user = response.json['user']
		print(user)
		print(type(user))
		self.assertEqual(user.get('first_name'), new_data.get('first_name'))
		self.assertEqual(user.get('last_name'), new_data.get('last_name'))
		self.assertEqual(user.get('email'), new_data.get('email'))

		# delete teh users
		self.tester.delete('/api/v1/users', headers={"Authorization": f"Bearer {access_token}"})

	def test_delete_user(self):
		# Register and login to get access token
		self.tester.post('/api/v1/register', json=self.test_user)
		login_response = self.tester.post('/api/v1/login', json={
			"email": self.test_user['email'],
			"password": self.test_user['password']
		})
		access_token = login_response.json['access_token']
		response = self.tester.delete('/api/v1/users', headers={"Authorization": f"Bearer {access_token}"})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json['status'], 'success')

	def tearDown(self):
		# Cleanup test user if exists

		# first user
		login_response = self.tester.post('/api/v1/login', json={
			"email": self.test_user['email'],
			"password": self.test_user['password']
		})
		if login_response.status_code == 200:
			access_token = login_response.json['access_token']
			self.tester.delete('/api/v1/users', headers={"Authorization": f"Bearer {access_token}"})

		# second user
		login_response = self.tester.post('/api/v1/login', json={
			"email": self.test_user2['email'],
			"password": self.test_user2['password']
		})
		if login_response.status_code == 200:
			access_token = login_response.json['access_token']
			self.tester.delete('/api/v1/users', headers={"Authorization": f"Bearer {access_token}"})


if __name__ == "__main__":
	unittest.main()
