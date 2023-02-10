"""
Tests for the Tags API
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Tag

from recipe.serializers import (TagSerializer)

TAGS_URL = reverse('recipe:tag-list')

def detail_url(tag_id):
	"""Create and return a tag detail url"""
	return reverse('recipe:tag-detail',args=[tag_id])

def create_user(email='user@example.com', password='testpass123'):
	"""Create and return a new user."""

	return get_user_model().objects.create_user(email,password)


class PublicTAGAPITests(TestCase):
	"""Test unauthenticated API requests"""

	def setUp(self):
		self.client = APIClient()

	def test_auth_required(self):
		"""Test auth is required to call API"""

		res = self.client.get(TAGS_URL)

		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
	"""Test authenticated API requests"""

	def setUp(self):
		self.client = APIClient()
		self.user = create_user()
		self.client.force_authenticate(self.user)

	def test_retrieve_tags(self):
		"""Test retrievinf a list of tag"""

		Tag.objects.create(user=self.user, name="Vegan")
		Tag.objects.create(user=self.user, name="Dessert")

		res = self.client.get(TAGS_URL)

		tags = Tag.objects.all().order_by('-name')
		serializer = TagSerializer(tags, many=True)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data,serializer.data)

	def test_tag_list_limited_to_user(self):
		"""Test retrieving a list of tags"""

		other_user =create_user(email='other@example.com', password= 'testpass123')

		tag = Tag.objects.create(user=self.user, name="Vegan")
		Tag.objects.create(user=other_user, name="Dessert")

		res = self.client.get(TAGS_URL)

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data[0]['name'], tag.name)
		self.assertEqual(res.data[0]['id'], tag.id)
		self.assertEqual(len(res.data), 1)

	def test_update_tag(self):
			"""Test full update of a recipe"""

			tag = Tag.objects.create(user=self.user, name="Dessert")

			payload = {
				'name': 'Sample recipe',
			}

			url = detail_url(tag.id)

			res = self.client.put(url, payload)

			self.assertEqual(res.status_code,status.HTTP_200_OK)
			tag.refresh_from_db()
			self.assertEqual(tag.name , payload['name'])

	def test_delete_tag(self):
			"""Test full update of a recipe"""

			tag = Tag.objects.create(user=self.user, name="Dessert")

			url = detail_url(tag.id)

			res = self.client.delete(url)

			self.assertEqual(res.status_code,status.HTTP_204_NO_CONTENT)
			tags = Tag.objects.filter(user=self.user)
			self.assertFalse(tags.exists())



