from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='level-test-home'),
    path('about/', views.about, name='level-test-about'),
    path('start-test/', views.start_test, name='start_test'),
    path('kanji-test/', views.kanji_test, name='kanji_test'),
    path('test-results/', views.test_results, name='test_results'),
]
