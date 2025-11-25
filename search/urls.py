from django.urls import path
from . import views

urlpatterns = [
    path('image/', views.search_by_image, name='search-image'),
    path('text/', views.search_by_text, name='search-text'),
    path('history/', views.get_search_history, name='search-history'),
    path('history/delete/', views.delete_search_history, name='search-history-delete'),
]
