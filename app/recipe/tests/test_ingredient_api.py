from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core import models
from recipe import serializers


INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@borna.com',
            password='password'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):

        models.Ingredient.objects.create(user=self.user, name='ing1')
        models.Ingredient.objects.create(user=self.user, name='ing2')

        res = self.client.get(INGREDIENT_URL)
        ingredients = models.Ingredient.objects.all().order_by('-name')

        serializer = serializers.IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limitted_to_user(self):

        another_user = get_user_model().objects.create_user(
            email='test2@gmail.com',
            password='password'
        )

        models.Ingredient.objects.create(user=another_user, name='cocumber')
        ingredient = models.Ingredient.objects.create(
            user=self.user, name='potato')
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'] , ingredient.name)
