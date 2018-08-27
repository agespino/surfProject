from django.urls import path

from . import views


app_name = 'visualize'

urlpatterns = [
    path('visualize/<str:queryType>/<str:query>', views.visualize, name = 'visualize')
]