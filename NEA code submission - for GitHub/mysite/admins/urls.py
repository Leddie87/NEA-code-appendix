from django.urls import path
from . import views

urlpatterns = [
    path('useraccs/', views.useraccs, name='useraccs'),
    path('home/', views.home, name='home'),
    path('trading/', views.trading, name='trading'),
    path('med_mark/', views.med_mark, name='med_mark'),
    path('finances/', views.finances, name='finances'),
    path('fairs/', views.fairs, name='fairs'),
    path('accepted/', views.accepted, name='accepted'),
    path('denied/', views.denied, name='denied'),
    path('apcinfo/', views.apcinfo, name='apcinfo'),
    path('email/', views.email, name='email'),
    path('gone/', views.gone, name='gone'),
]