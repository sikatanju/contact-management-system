from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detail/<int:pk>', views.contact_detail, name='contact-detail'),
    path('login/', views.authorize_admin, name='authorize-admin'),
    path('logout/', views.unauthorize_admin, name='unauthorize-admin'),
    path('add/', views.add_contact,name='add-contact'),
    path('update/', views.update_contact_list, name='update-contact-list'),
    path('update/<int:pk>', views.update_an_contact, name='update-contact'),
    path('delete/', views.delete_contact_list, name='delete-contact-list'),
    path('delete/<int:pk>', views.delete_an_contact, name='delete-contact'),
]