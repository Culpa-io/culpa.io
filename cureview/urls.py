from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    # path('compare', views.compare, name='compare'),
    path('reviews/<str:category>/<int:id>', views.reviews, name='reviews'),
    path('compose', views.compose, name='compose'),
    path('getrodata', views.getrodata, name='getrodata'),
    path('submitreview', views.submitreview, name='submitreview'),
    path('search-opt', views.searchOpt, name='search-opt'),
    path('core-data-query', views.coreDataQuery, name='core-data-query')
]
