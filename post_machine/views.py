from django.http import HttpResponse
from django.shortcuts import render

from post_machine.models import PostMachine, Locker
from parcel.models import Parcel


def post_machines_list_view(request):
    post_machines = PostMachine.objects.all()
    if post_machines is None:
        return HttpResponse("Cannot find any post machine.")
    pm_str = ', '.join([f'id: {pm.id}, city: {pm.city}' for pm in post_machines])
    # return render(request, 'post_machines_list.html', {post_machines:post_machines})
    return HttpResponse(f"Post machines list: {pm_str}")


def post_machine_view(request, post_machine_id):
    post_machine = PostMachine.objects.get(pk=post_machine_id)
    if post_machine is None:
        return HttpResponse(f"Cannot find a post machine with id {post_machine}.")
    # return render(request, 'post_machine.html')
    return HttpResponse(f"Post machine info: id: {post_machine_id} city: {post_machine.city}")


def lockers_view(request, post_machine_id):
    post_machine = PostMachine.objects.get(pk=post_machine_id)
    if post_machine is None:
        return HttpResponse(f"Cannot find a post machine with id {post_machine}.")
    lockers = post_machine.lockers.all()
    if lockers is None:
        return HttpResponse(f"Cannot find any locker in the post machine {post_machine_id}.")
    lockers_str = ', '.join([f'id: {locker.id} size: {locker.size} status: {locker.status}' for locker in lockers])
    # return render(request, 'post_machine_lockers.html')
    return HttpResponse(f"Post machine {post_machine_id} lockers: {lockers_str}")


def locker_view(request, post_machine_id, locker_id):
    post_machine = PostMachine.objects.get(pk=post_machine_id)
    if post_machine is None:
        return HttpResponse(f"Cannot find a post machine with id {post_machine}.")
    locker = Locker.objects.filter(post_machine=post_machine, pk=locker_id)
    if locker is None:
        return HttpResponse(f"Cannot find a locker with id {locker_id} in the post machine {post_machine_id}.")
    # return render(request, 'post_machine_locker.html')
    return HttpResponse(f"Post machine {post_machine_id} locker {locker_id}"
                        f" size: {locker.size} status: {locker.status}")


def post_machine_parcels_view(request, post_machine_id):
    post_machine = PostMachine.objects.get(pk=post_machine_id)
    if post_machine is None:
        return HttpResponse(f"Cannot find a post machine with id {post_machine}.")
    parcels = Parcel.objects.filter(post_machine_locker__post_machine=post_machine)
    if parcels is None:
        return HttpResponse(f"Cannot find any parcel in the post machine {post_machine_id}.")
    # return render(request, 'parcel.html')
    parcels_str = ', '.join([f'id: {parcel.id}, sender: {parcel.sender}, size: {parcel.size}' for parcel in parcels])
    return HttpResponse(f"Post machine {post_machine_id} parcels {parcels_str}")


def post_machine_parcel_view(request, post_machine_id, parcel_id):
    post_machine = PostMachine.objects.get(pk=post_machine_id)
    if post_machine is None:
        return HttpResponse(f"Cannot find a post machine with id {post_machine}.")
    parcel = Parcel.objects.get(post_machine_locker__post_machine=post_machine, pk=parcel_id)
    if parcel is None:
        return HttpResponse(f"Cannot find a locker with id {parcel_id} in the post machine {post_machine_id}.")
    # return render(request, 'parcel.html')
    return HttpResponse(f"Post machine {post_machine_id} Parcel {parcel_id} info: id: {parcel.id},"
                        f" sender: {parcel.sender}, size: {parcel.size}")
