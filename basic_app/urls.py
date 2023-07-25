from django.urls import path
from .views import ListFile, ListFile2

urlpatterns = [
    path('file_2021/', ListFile.as_view()),
    path('file_2022/', ListFile2.as_view()),
]