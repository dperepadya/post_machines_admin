from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from parcel.models import Parcel


@login_required(login_url='/login/')
def parcels_list_view(request):
    parcels = Parcel.objects.all()
    if parcels is None:
        return HttpResponse("Cannot find any parcel.")
    return render(request, 'parcels_list.html', {'parcels': parcels})
    # parcels_str = ', '.join([f'id: {parcel.id}, sender: {parcel.sender}, size: {parcel.size}' for parcel in parcels])
    # return HttpResponse(f"Parcels list: {parcels_str}")


@login_required(login_url='/login/')
def parcel_view(request, parcel_id):
    parcel = Parcel.objects.get(pk=parcel_id)
    if parcel is None:
        return HttpResponse(f"Cannot find a parcel with id {parcel_id}.")
    return render(request, 'parcel.html', {'parcel': parcel})
    # return HttpResponse(f"Parcel {parcel_id} info: {parcel.id}, sender: {parcel.sender}, size: {parcel.size}")

