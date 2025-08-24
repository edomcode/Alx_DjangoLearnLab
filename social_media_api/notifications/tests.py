from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from posts.models import Post, Like
from notifications.models import Notification
# Create your tests here.


class LikesNotificationsTests(APITestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        # Create a post by user2
        self.post = Post.objects.create(author=self.user2, title='Test Post', content='Content')

    def test_like_post_creates_notification(self):
        self.client.login(username='user1', password='pass123')
        url = reverse('post-like', args=[self.post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check Like created
        self.assertTrue(Like.objects.filter(user=self.user1, post=self.post).exists())
        # Check Notification created
        self.assertTrue(Notification.objects.filter(recipient=self.user2, actor=self.user1).exists())

    def test_unlike_post(self):
        self.client.login(username='user1', password='pass123')
        Like.objects.create(user=self.user1, post=self.post)
        url = reverse('post-unlike', args=[self.post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Like.objects.filter(user=self.user1, post=self.post).exists())

    def test_cannot_like_twice(self):
        self.client.login(username='user1', password='pass123')
        Like.objects.create(user=self.user1, post=self.post)
        url = reverse('post-like', args=[self.post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_notifications_endpoint(self):
        self.client.login(username='user2', password='pass123')
        Notification.objects.create(recipient=self.user2, actor=self.user1, verb="liked your post", target=self.post)
        url = reverse('notifications-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)