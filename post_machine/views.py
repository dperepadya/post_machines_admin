from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def post_machines_list_view(request):
    # return render(request, 'post_machines_list.html')
    return HttpResponse("Hello, world. You're at the post machines list view.")


def post_machine_view(request, post_machine_id):
    # return render(request, 'post_machine.html')
    return HttpResponse(f"Hello, world. You're at the post machine {post_machine_id} view.")


def lockers_view(request, post_machine_id):
    # return render(request, 'post_machine.html')
    return HttpResponse(f"Hello, world. You're at the post machine {post_machine_id} lockers view.")


def locker_view(request, post_machine_id, locker_id):
    # return render(request, 'post_machine.html')
    return HttpResponse(f"Hello, world. You're at the post machine {post_machine_id} locker {locker_id} view.")