from django.contrib import admin
from django.urls import path
from scraper.views import StartScrapingView, ScrapingStatusView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('taskmanager/start_scraping/', StartScrapingView.as_view()),
    path('taskmanager/status/<int:job_id>/', ScrapingStatusView.as_view()),
]
