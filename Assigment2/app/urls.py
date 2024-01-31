from django.urls import path
from . import views

urlpatterns = [
    path('entries/', views.EntryListCreate.as_view(), name='entry-list-create'),
    path('entries/<int:pk>/', views.EntryRetrieveUpdateDestroy.as_view(), name='entry-retrieve-update-destroy'),
]
