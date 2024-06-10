from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job, Task
from .serializers import JobSerializer, TaskSerializer, CryptoRequestSerializer
from .coinmarketcap import CoinMarketCap # type: ignore
from celery import shared_task
from celery.result import AsyncResult

@shared_task
def scrape_coin(coin_name):
    cmc = CoinMarketCap()
    data = cmc.scrape_coin(coin_name)
    return data

class StartScrapingView(APIView):
    def post(self, request):
        serializer = CryptoRequestSerializer(data=request.data)
        if serializer.is_valid():
            coins = serializer.validated_data['coins']
            job = Job.objects.create()
            job_serializer = JobSerializer(job)
            for coin in coins:
                task = Task.objects.create(job=job, coin=coin)
                scrape_coin.delay(coin)
            return Response(job_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        try:
            job = Job.objects.get(pk=job_id)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        tasks = Task.objects.filter(job=job)
        task_serializer = TaskSerializer(tasks, many=True)

        for task in tasks:
            result = AsyncResult(task.task_id)
            if result.ready():
                task.output = result.get()
                task.save()

        return Response(task_serializer.data, status=status.HTTP_200_OK)

