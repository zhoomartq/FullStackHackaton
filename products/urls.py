from django.urls import path
from . import views
from .views import CategoryListView, CategoryDetailView

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('categories/<str:pk>/', CategoryDetailView.as_view()),
    path('favorites/', views.FavoriteListView.as_view()),
]
