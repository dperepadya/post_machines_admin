from django.urls import path

import parcel
import post_machine.views

urlpatterns = [
    path('', post_machine.views.post_machines_list_view, name='post_machines_list_view'),
    path('<int:post_machine_id>/', post_machine.views.post_machine_view, name='post_machine_view'),
    path('<int:post_machine_id>/lockers/', post_machine.views.lockers_view, name='lockers_view'),
    path('<int:post_machine_id>/lockers/<int:locker_id>/', post_machine.views.locker_view, name='locker_view'),
    path('<int:post_machine_id>/parcels/', post_machine.views.post_machine_parcels_view,
         name='post_machine_parcels_view'),
    path('<int:post_machine_id>/parcels/<int:parcel_id>/', post_machine.views.post_machine_parcel_view,
         name='post_machine_parcel_view'),
]