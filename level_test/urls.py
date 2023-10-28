from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='level-test-home'),
    path('about/', views.about, name='level-test-about'),
    path('start-test/', views.start_test, name='start_test'),
    path('kanji-test/', views.kanji_test, name='kanji_test'),
    path('test-complete/', views.test_complete, name='test_complete'),
    path('test-failed/', views.test_failed, name='test_failed'),
    # path('study', views.study, name='level-test-study'),
]
