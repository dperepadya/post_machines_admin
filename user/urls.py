from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_page, name='user'),
    path('parcels/', views.user_parcels_view, name='user_parcels'),
    path('parcels/<int:parcel_id>/', views.user_parcel_view, name='user_parcel'),
    path('parcels/<int:parcel_id>/edit/', views.user_parcel_edit, name='user_parcel_edit'),
    path('parcels/create/', views.user_parcel_create, name='user_parcel_create'),

    path('parcels/select_recipient/', views.select_recipient_and_post_machine, name='select_recipient'),
    # path('parcels/select_post_machine/', views.select_post_machine, name='select_post_machine'),
    path('parcels/select_locker/', views.select_locker, name='select_locker'),
    path('parcels/<int:parcel_id>/pick_up/', views.user_parcel_pick_up, name='user_parcel_pick_up'),

]