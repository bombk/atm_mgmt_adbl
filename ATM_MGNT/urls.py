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
    path('atmdown_list', views.file_transfer_down, name='atmdown_list'),
    path('contact', views.contact_list, name='contact'),
    path('add_atmdown',views.add_atmdown,name='add_atmdown'),
    path('atm_down_list',views.atm_down_list,name='atm_down_list'),
    path('update_atmdown/<int:id>',views.update_atmdown,name='update_atmdown'),
    path('past_atm_down_list',views.past_atm_down_list,name='past_atm_down_list'),
    path('vendor_contact',views.vendor_contact,name='vendor_contact'),
]