""""Authentication Module"""

# Requests
import requests

# Json
import json

class Authentication:
	"""Manages all the taks related with authenticate the user."""

	def __init__(self):
		self.session = requests.Session()
		self.session.headers.update(
			{
				"Content-Type": "application/json"
			}
		)

	def login(self, username, password):

		session = self.session

		payload = {
			'username': username,
			'password': password
		}

		request = session.post('https://iptvfilecleaner.me/users/login/', data=json.dumps(payload))

		response = request.json()

		if response.get('access', False):

			token = response.get('access')
			session.headers.update({
					'Authorization': f'JWT {token}'
				})
			self.session = session
			return True
		else:
			return False

	def is_user_premium(self, username):
		""""Returns if a user is premium."""

		session = self.session

		url = f'https://iptvfilecleaner.me/users/{username}/'
		request = session.get(url)

		response = request.json()

		is_premium = response.get('is_premium')

		return is_premium

