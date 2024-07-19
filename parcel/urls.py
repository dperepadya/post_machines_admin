from django.urls import path

import parcel.views

urlpatterns = [
    path('', parcel.views.parcels_list_view, name='parcels_list'),
    path('<int:parcel_id>/', parcel.views.parcel_view, name='parcel'),
]
