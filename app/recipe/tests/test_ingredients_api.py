"""
Tests for the Ingredients API
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Ingredient

from recipe.serializers import (IngredientSerializer)

INGREDIENTS_URL = reverse('recipe:ingredient-list')

def detail_url(ingredient_id):
	"""Create and return a ingredient detail url"""
	return reverse('recipe:ingredient-detail',args=[ingredient_id])

def create_user(email='user@example.com', password='testpass123'):
	"""Create and return a new user."""

	return get_user_model().objects.create_user(email,password)


class PublicINGREDIENTAPITests(TestCase):
	"""Test unauthenticated API requests"""

	def setUp(self):
		self.client = APIClient()

	def test_auth_required(self):
		"""Test auth is required to call API"""

		res = self.client.get(INGREDIENTS_URL)

		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeAPITests(TestCase):
	"""Test authenticated API requests"""

	def setUp(self):
		self.client = APIClient()
		self.user = create_user()
		self.client.force_authenticate(self.user)

	def test_retrieve_ingredients(self):
		"""Test retrievinf a list of ingredient"""

		Ingredient.objects.create(user=self.user, name="Kale")
		Ingredient.objects.create(user=self.user, name="Vanilla")

		res = self.client.get(INGREDIENTS_URL)

		ingredients = Ingredient.objects.all().order_by('-name')
		serializer = IngredientSerializer(ingredients, many=True)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data,serializer.data)

	def test_ingredient_list_limited_to_user(self):
		"""Test retrieving a list of ingredients"""

		other_user =create_user(email='other@example.com', password= 'testpass123')

		ingredient = Ingredient.objects.create(user=self.user, name="Kale")
		Ingredient.objects.create(user=other_user, name="Vanilla")

		res = self.client.get(INGREDIENTS_URL)

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data[0]['name'], ingredient.name)
		self.assertEqual(res.data[0]['id'], ingredient.id)
		self.assertEqual(len(res.data), 1)

	def test_update_ingredient(self):
			"""Test full update of a recipe"""

			ingredient = Ingredient.objects.create(user=self.user, name="Cilantro")

			payload = {
				'name': 'Coriander',
			}

			url = detail_url(ingredient.id)

			res = self.client.put(url, payload)

			self.assertEqual(res.status_code,status.HTTP_200_OK)
			ingredient.refresh_from_db()
			self.assertEqual(ingredient.name , payload['name'])

	def test_delete_ingredient(self):
			"""Test full update of a recipe"""

			ingredient = Ingredient.objects.create(user=self.user, name="Dessert")

			url = detail_url(ingredient.id)

			res = self.client.delete(url)

			self.assertEqual(res.status_code,status.HTTP_204_NO_CONTENT)
			ingredients = Ingredient.objects.filter(user=self.user)
			self.assertFalse(ingredients.exists())

