from django.urls import path
from . import views

urlpatterns = [
    path('', views.study, name='study'),
    path('deck/', views.deck, name='study-deck'),
    # path('start-test/', views.start_test, name='start_test'),
    # path('kanji-test/', views.kanji_test, name='kanji_test'),
    # path('test-results/', views.test_results, name='test_results'),
]
