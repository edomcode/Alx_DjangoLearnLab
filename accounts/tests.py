from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

class FollowFeedTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="password123")
        self.user2 = User.objects.create_user(username="bob", password="password123")

        response = self.client.post(reverse("login"), {
            "username": "alice",
            "password": "password123"
        })
        self.token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_follow_user(self):
        url = reverse("user-follow", kwargs={"pk": self.user2.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("You are now following", response.data["detail"])

    def test_unfollow_user(self):
    
        self.user1.following.add(self.user2)
        url = reverse("user-unfollow", kwargs={"pk": self.user2.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("You have unfollowed", response.data["detail"])

    def test_feed_shows_followed_posts(self):
        post = Post.objects.create(author=self.user2, title="Hello", content="Bob's post")

        self.user1.following.add(self.user2)

        url = reverse("user-feed")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], post.title)

    def test_feed_empty_if_not_following(self):
        Post.objects.create(author=self.user2, title="Secret", content="Hidden")
        url = reverse("user-feed")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)