from django.urls import path

from . import views

app_name = 'places'
urlpatterns = [
    # ex: /places/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /places/1/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /places/1/review/
    path('<int:pk>/review/', views.ReviewView.as_view(), name='review'),
    # ex: /places/1/# REVIEW: /
    path('<int:place_id>/postreview/', views.postreview, name='postreview'),
]
