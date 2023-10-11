from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='level-test-home'),
    path('about/', views.about, name='level-test-about'),
    path('kanji_test/', views.kanji_test, name='level-test-kanji-test'),
    # path('study', views.study, name='level-test-study'),
]
