""""Authentication Module"""

# Requests
import requests


class Authentication:
	"""Manages all the taks related with authenticate the user."""

	def __init__(session):
		self.session = request.Session()

	def login(username, password):

		session = self.session

		payload = {
			'email': email,
			'password': password
		}

		request = session.post('http://localhost:8000/users/login/', payload)

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

	def is_user_premium(username):
		""""Returns if a user is premium."""

		session = self.session

		url = f'http://localhost:8000/users/{username}/'
		request = session.get(url)

		response = request.json()

		is_premium = request.get('is_premium')

		return is_premium

