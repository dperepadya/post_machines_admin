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
    # pm_str = ', '.join([f'id: {pm.id}, city: {pm.city}' for pm in post_machines])
    # return HttpResponse(f"Post machines list: {pm_str}")


# @user_passes_test(is_superuser, login_url='/login/')
def post_machine_view(request, post_machine_id):
    post_machine = PostMachine.objects.get(pk=post_machine_id)
    if post_machine is None:
        return HttpResponse(f"Cannot find a post machine with id {post_machine}.")
    return render(request, 'post_machine.html', {'post_machine': post_machine})
    # return HttpResponse(f"Post machine info: id: {post_machine_id} city: {post_machine.city}")


@user_passes_test(is_superuser, login_url='/login/')
def lockers_view(request, post_machine_id):
    post_machine = PostMachine.objects.get(pk=post_machine_id)
    if post_machine is None:
        return HttpResponse(f"Cannot find a post machine with id {post_machine}.")
    lockers = post_machine.lockers.all()
    if lockers is None:
        return HttpResponse(f"Cannot find any locker in the post machine {post_machine_id}.")
    return render(request, 'lockers_list.html', {'post_machine': post_machine, 'lockers': lockers})
    # lockers_str = ', '.join([f'id: {locker.id} size: {locker.size} status: {locker.status}' for locker in lockers])
    # return HttpResponse(f"Post machine {post_machine_id} lockers: {lockers_str}")


@user_passes_test(is_superuser, login_url='/login/')
def locker_view(request, post_machine_id, locker_id):
    post_machine = PostMachine.objects.get(pk=post_machine_id)
    if post_machine is None:
        return HttpResponse(f"Cannot find a post machine with id {post_machine}.")
    locker = Locker.objects.get(post_machine=post_machine, pk=locker_id)
    if locker is None:
        return HttpResponse(f"Cannot find a locker with id {locker_id} in the post machine {post_machine_id}.")
    return render(request, 'locker.html', {'post_machine': post_machine, 'locker': locker})
    # return HttpResponse(f"Post machine {post_machine_id} locker {locker_id}"
    #                     f" size: {locker.size} status: {locker.status}")


@user_passes_test(is_superuser, login_url='/login/')
def post_machine_parcels_view(request, post_machine_id):
    post_machine = PostMachine.objects.get(pk=post_machine_id)
    if post_machine is None:
        return HttpResponse(f"Cannot find a post machine with id {post_machine}.")
    parcels = Parcel.objects.filter(post_machine_locker__post_machine=post_machine)
    #l ogging.info(f"Parcels queryset: {parcels}")
    print(parcels)
    if parcels is None:
        return HttpResponse(f"Cannot find any parcel in the post machine {post_machine_id}.")
    # for parcel in parcels:
        # pdb.set_trace()  # Set another breakpoint to inspect each parcel
        # Print or inspect parcel attributes
        # s_time = datetime.datetime.fromtimestamp(parcel.send_date_time / 1000.0)
        # print(f"Parcel ID: {parcel.id}, Send Date and Time: {s_time}")

    context = {'post_machine': post_machine, 'parcels': parcels}
    return render(request, 'parcels_list.html', context)
    # parcels_str = ', '.join([f'id: {parcel.id}, sender: {parcel.sender}, size: {parcel.size}' for parcel in parcels])
    # return HttpResponse(f"Post machine {post_machine_id} parcels {parcels_str}")


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
    # return HttpResponse(f"Post machine {post_machine_id} Parcel {parcel_id} info: id: {parcel.id},"
    #                     f" sender: {parcel.sender}, size: {parcel.size}")

