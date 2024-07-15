from django.http import HttpResponse
from django.shortcuts import render

from parcel.models import Parcel


def parcels_list_view(request):
    parcels = Parcel.objects.all()
    if parcels is None:
        return HttpResponse("Cannot find any parcel.")
    # return render(request, 'parcels_list.html')
    parcels_str = ', '.join([f'id: {parcel.id}, sender: {parcel.sender}, size: {parcel.size}' for parcel in parcels])
    return HttpResponse(f"Parcels list: {parcels_str}")


def parcel_view(request, parcel_id):
    parcel = Parcel.objects.get(pk=parcel_id)
    if parcel is None:
        return HttpResponse(f"Cannot find a parcel with id {parcel_id}.")
    # return render(request, 'parcel.html')
    return HttpResponse(f"Parcel {parcel_id} info: {parcel.id}, sender: {parcel.sender}, size: {parcel.size}")

