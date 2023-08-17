import time

from django.core.cache import cache
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Post


class PostCreationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_post_creation(self):
        response = self.client.post('/api/v1/posts/', {'content': 'test content'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue('unique_id' in response.data)
        self.assertTrue(Post.objects.filter(unique_id=response.data['unique_id']).exists())


class PostAnalysisTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_post_analysis(self):
        self.post = Post.objects.create(content='This is a test post.')
        response = self.client.get(f'/api/v1/posts/{self.post.unique_id}/analysis/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'word_count': 5, 'average_word_length': 3})

    def test_post_analysis2(self):
        self.post = Post.objects.create(content='This is a test post, And want to remove punctuations. Okay!')
        response = self.client.get(f'/api/v1/posts/{self.post.unique_id}/analysis/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'word_count': 11, 'average_word_length': 4.181818181818182})



class PostAnalysisCachingTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.post = Post.objects.create(content='This is another test post.')

    def test_post_analysis_caching(self):
        start_time = time.time()
        response = self.client.get(f'/api/v1/posts/{self.post.unique_id}/analysis/')
        first_request_time = time.time() - start_time

        start_time = time.time()
        response = self.client.get(f'/api/v1/posts/{self.post.unique_id}/analysis/')
        second_request_time = time.time() - start_time

        self.assertLess(second_request_time, first_request_time)




class PostRetrievalTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.posts = [Post.objects.create(content=f'test content {i}') for i in range(5)]

    def test_post_retrieval(self):
        response = self.client.get('/api/v1/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(self.posts))


class ThrottleTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        cache.clear()

    def test_throttle(self):
        for i in range(105):  # Assuming the throttle limit is 100 requests per hour
            response = self.client.get('/api/v1/posts/')
        self.assertEqual(response.status_code, 429)  # HTTP 429 Too Many Requests
