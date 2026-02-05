from django.urls import path
from . import views

app_name = 'register'

urlpatterns = [    
    path('adlog/', views.adlog, name='adlog'),    
    path('aplog/', views.aplog, name='aplog'),    
    path('sign/' ,views.sign,   name = 'sign'),    ]