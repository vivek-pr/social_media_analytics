from django.urls import path
from .views import PostCreateView, PostAnalysisView

urlpatterns = [
    path('posts/', PostCreateView.as_view(), name='post-list-create'),
    path('posts/<str:id>/analysis/', PostAnalysisView.as_view(), name='post-analysis'),
]
