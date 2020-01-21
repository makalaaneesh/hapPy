from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wordcloud', views.wordcloud, name="wordcloud")
]
