from django.urls import path

from . import views


app_name = 'search'

urlpatterns = [
    path('', views.index, name='index'),
    path('results/<str:queryType>/<str:query>', views.results, name = 'search-results'),
    path('resultsList/<str:queryType>/<str:query>', views.resultsLstView, name = 'search-results-list')
]