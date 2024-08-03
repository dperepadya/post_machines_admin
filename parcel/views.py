from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from parcel.models import Parcel


@login_required(login_url='/login/')
def parcels_list_view(request):
    try:
        parcels = Parcel.objects.all()
        return render(request, 'parcels_list.html', {'parcels': parcels})
    except Parcel.DoesNotExist:
        return JsonResponse({'error': f"CCannot find any parcel."}, status=404)


@login_required(login_url='/login/')
def parcel_view(request, parcel_id):
    try:
        parcel = Parcel.objects.get(pk=parcel_id)
        return render(request, 'parcel.html', {'parcel': parcel})
    except Parcel.DoesNotExist:
        return JsonResponse({'error': f"Cannot find a parcel with id {parcel_id}"}, status=404)



