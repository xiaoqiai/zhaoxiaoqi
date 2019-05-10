from django.urls import path
from .import views
urlpatterns=[
    path('index2/',views.index2,name='index2')
]