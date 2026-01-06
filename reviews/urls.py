# reviews/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_review_api, name='api-submit-review'),
]