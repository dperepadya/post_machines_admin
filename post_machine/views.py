import logging
import pdb
import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render

from post_machine.models import PostMachine, Locker
from parcel.models import Parcel
from utils import is_superuser


# @user_passes_test(is_superuser, login_url='/login/')
def post_machines_list_view(request):
    post_machines = PostMachine.objects.all()
    if post_machines is None:
        return HttpResponse("Cannot find any post machine.")
    return render(request, 'post_machines_list.html', {'post_machines': post_machines})


# @user_passes_test(is_superuser, login_url='/login/')
def post_machine_view(request, post_machine_id):
    post_machine = PostMachine.objects.get(pk=post_machine_id)
    if post_machine is None:
        return HttpResponse(f"Cannot find a post machine with id {post_machine}.")
    return render(request, 'post_machine.html', {'post_machine': post_machine})


@user_passes_test(is_superuser, login_url='/login/')
def lockers_view(request, post_machine_id):
    post_machine = PostMachine.objects.get(pk=post_machine_id)
    if post_machine is None:
        return HttpResponse(f"Cannot find a post machine with id {post_machine}.")
    lockers = post_machine.lockers.all()
    if lockers is None:
        return HttpResponse(f"Cannot find any locker in the post machine {post_machine_id}.")
    return render(request, 'lockers_list.html', {'post_machine': post_machine, 'lockers': lockers})


@user_passes_test(is_superuser, login_url='/login/')
def locker_view(request, post_machine_id, locker_id):
    post_machine = PostMachine.objects.get(pk=post_machine_id)
    if post_machine is None:
        return HttpResponse(f"Cannot find a post machine with id {post_machine}.")
    locker = Locker.objects.get(post_machine=post_machine, pk=locker_id)
    if locker is None:
        return HttpResponse(f"Cannot find a locker with id {locker_id} in the post machine {post_machine_id}.")
    return render(request, 'locker.html', {'post_machine': post_machine, 'locker': locker})


@user_passes_test(is_superuser, login_url='/login/')
def post_machine_parcels_view(request, post_machine_id):
    post_machine = PostMachine.objects.get(pk=post_machine_id)
    if post_machine is None:
        return HttpResponse(f"Cannot find a post machine with id {post_machine}.")
    parcels = Parcel.objects.filter(post_machine_locker__post_machine=post_machine)
    print(parcels)
    if parcels is None:
        return HttpResponse(f"Cannot find any parcel in the post machine {post_machine_id}.")
    context = {'post_machine': post_machine, 'parcels': parcels}
    return render(request, 'parcels_list.html', context)


@login_required
def post_machine_parcel_view(request, post_machine_id, parcel_id):
    post_machine = PostMachine.objects.get(pk=post_machine_id)
    if post_machine is None:
        return HttpResponse(f"Cannot find a post machine with id {post_machine}.")
    parcel = Parcel.objects.get(post_machine_locker__post_machine=post_machine, pk=parcel_id)
    if parcel is None:
        return HttpResponse(f"Cannot find a parcel with id {parcel_id} in the post machine {post_machine_id}.")
    context = {'post_machine': post_machine, 'parcel': parcel}
    return render(request, 'parcel.html', context)


