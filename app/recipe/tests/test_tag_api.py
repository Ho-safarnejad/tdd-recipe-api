from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from core.models import Tag
from rest_framework.test import APIClient
from rest_framework import status
from recipe.serializers import TagSerializer


TAG_URL = reverse('recipe:tag-list')


class PublicTagApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):

        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@borna.com', password='password')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retreive_tags(self):
        Tag.objects.create(user=self.user, name='vegan')
        Tag.objects.create(user=self.user, name='desert')
        res = self.client.get(TAG_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limitted_to_user(self):

        another_user = get_user_model().objects.create_user(
            email='another@borna.com',
            password='another_pass'
        )

        Tag.objects.create(user=another_user, name='fruity')
        tag = Tag.objects.create(user=self.user, name='drinks')

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successfull(self):

        payload = {'name': 'some name'}
        self.client.post(TAG_URL, payload)

        exist = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exist)

    def test_create_tag_invalid(self):
 
        payload = {'name': ''}
        res = self.client.post(TAG_URL, payload)
        self.assertEqual(res.status_code , status.HTTP_400_BAD_REQUEST)
