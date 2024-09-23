from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('atmlist', views.atm_list, name='atmlist'),
    path('atmdown', views.atm_down, name='atmdown'),
    path('atmdown_save', views.atm_down_save, name='atmdown_save'),
    path('get_atm', views.get_atm, name='get_atm'),
    path('atmdown_list', views.atm_down_list, name='atmdown_list'),
    path('contact', views.contact_list, name='contact'),
]