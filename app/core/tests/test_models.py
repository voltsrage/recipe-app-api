"""
Tests from models
"""
from decimal import Decimal
from django.test import TestCase
# always use this to get the user model
from django.contrib.auth import get_user_model

from core import models

class ModelTests(TestCase):
	'''Test Models'''

	def test_create_user_with_email_successful(self):
		"""Test creating a user with an email is successful"""

		email = 'test@example.com'
		password = 'password112'
		print('start')
		user = get_user_model().objects.create_user(
			email=email,
			password=password,
		)
		print(user)
		self.assertEqual(user.email, email)
		self.assertTrue(user.check_password(password))

	def test_new_user_email_normalized(self):
		"""Test email is normalized for new users"""

		sample_emails =[
			['test1@EXAMPLE.COM','test1@example.com'],
			['Test2@Example.COM','Test2@example.com'],
			['TEST3@EXAMPLE.COM','TEST3@example.com'],
			['test4@example.COM','test4@example.com'],
		]

		for email, expected in sample_emails:
			user = get_user_model().objects.create_user(email,'sample123')
			self.assertEqual(user.email, expected)

	def test_new_user_without_email_raises_error(self):
		"""Test that creating a user without an email raises a ValueError."""


		with self.assertRaises(ValueError):
			get_user_model().objects.create_user('','password123')

	def test_create_superuser(self):
		"""Test creating a superuser"""

		user = get_user_model().objects.create_superuser('Test5@example.com','password123')

		self.assertTrue(user.is_superuser)
		self.assertTrue(user.is_staff)

	def test_create_recipe(self):
		"""Test creating a recipe is successfuk"""

		user = get_user_model().objects.create_user(
			email='test@example.com',
			password='test-user-password123',
			name='Test Name',
		)

		recipe = models.Recipe.objects.create(
			user=user,
			title='Sample recipe name',
			time_minutes=5,
			price=Decimal('5.50'),
			description='Sample recipe description'
		)

		self.assertEqual(str(recipe),recipe.title)