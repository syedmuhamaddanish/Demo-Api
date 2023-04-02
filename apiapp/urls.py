from django.urls import path
from . import views

urlpatterns = [
    path('who-made-me/', views.who_made_me, name='who-made-me'),
    path('number-to-word/', views.number_to_word, name='number-to-word'),
    path('get-word/<word>/', views.get_word, name='get-word'),
]