from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def parcels_list_view(request):
    # return render(request, 'parcels_list.html')
    return HttpResponse("Hello, world. You're at the parcels list view.")


def parcel_view(request, parcel_id):
    # return render(request, 'parcel.html')
    return HttpResponse(f"Hello, world. You're at the parcel {parcel_id} view.")
