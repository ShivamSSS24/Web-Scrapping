from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Job, Task

class CryptoScraperTestCase(TestCase):
    def setUp(self):

        self.client = APIClient()

    def test_start_scraping_view(self):
        url = reverse('start_scraping')
        data = {'coins': ['bitcoin', 'ethereum']}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 1)
        self.assertEqual(Task.objects.count(), 2)

    def test_scraping_status_view(self):
        job = Job.objects.create()
        task1 = Task.objects.create(job=job, coin='bitcoin')
        task2 = Task.objects.create(job=job, coin='ethereum')
        
        url = reverse('scraping_status', args=[job.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) 
        
    def tearDown(self):
        pass
