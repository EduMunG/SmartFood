from django.urls import path
from . import views

urlpatterns =[
    path('login/', views.user_login, name='login'),
    path('home/', views.home, name = 'home'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('takeData', views.takeData, name='takeData'),
    path('agregar_alimento/', views.agregar_alimento, name='agregar_alimento'),
    path('consumo/', views.consumo, name='consumo'), 
    path('buscar_alimento/', views.buscar_alimento, name='buscar_alimento'),
    path('cambiar_inf/', views.cambiar_inf, name='cambiar_inf'),

]