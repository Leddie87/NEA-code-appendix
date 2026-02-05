from django.urls import path
from . import views

urlpatterns = [
    path('form/', views.appform, name='appform'),
    path('apchome/', views.apchome, name='apchome'),
    path('gone/', views.gone, name='gone'),
    path('testform/', views.testform, name='testform'),
    path('fsub/', views.fsub, name='tfsub'),
   # path('nametest/', views.bigtest, name='bigtest'),
    
]
