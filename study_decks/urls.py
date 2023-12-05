from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('', views.study, name='study'),
    path('study/<int:jlpt_level>', views.study_level, name='study-level'),
]
