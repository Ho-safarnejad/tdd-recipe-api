from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
         """ test creating some user by email address. """
         email = 'test@gmail.com'
         password = 'Test2122012'
         user = get_user_model().objects.create_user(
         email=email ,
         password=password
         )

         self.assertEqual(user.email , email)
         self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):

         """ test creating new user with normilized email. """
         email = 'test2@GMAIL.COM'
         user = get_user_model().objects.create_user(email , 'test123')

         self.assertEqual(user.email , email.lower())


    def test_new_user_email_normalized(self):
         """ test creating new user with blank email. """

         with self.assertRaises(ValueError):
           get_user_model().objects.create_user(None , 'test123')


    def test_create_new_superuser(self):
         """ test create new superuser """
         user = get_user_model().objects.create_superuser(
         'test@gmail.com',
         'test123'
         )

         self.assertTrue(user.is_superuser)
         self.assertTrue(user.is_staff)