from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from parcel.models import Parcel
from post_machine.models import PostMachine, Locker
from user.forms import LoginForm, RegisterForm
from utils import is_superuser


class LoginView(View):
    def get(self, request):
        context = {'form': LoginForm()}
        return render(request, 'login.html', context=context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/user/')
            form.add_error(None, "Username or password is incorrect")
        else:
            form.add_error(None, "There was an error with your submission.")
        context = {'error': "Username or password is incorrect", 'form': form}
        return render(request, 'login.html', context)


'''
def login_page(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/user/')
        context = {'error': "Username or password is incorrect"}
    context['form'] = LoginForm()
    return render(request, 'login.html', context=context)
'''


@login_required
def logout_page(request):
    logout(request)
    return redirect('/login/')


class RegisterView(View):
    def get(self, request):
        context = {'form': RegisterForm()}
        return render(request, 'register.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                return redirect('/login/')
            except IntegrityError:
                form.add_error('username', 'Username is already taken.')
        context = {'form': form}
        return render(request, 'register.html', context)


'''
def register_page(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                return redirect('/login/')
            except IntegrityError:
                form.add_error('username', 'Username is already taken.')
        context = {'form': form}
        return render(request, 'register.html', context)
    else:
        context = {'form': RegisterForm()}
        return render(request, 'register.html', context)
'''


@login_required(login_url='/login/')
def user_page(request):
    context = {'user': request.user}
    return render(request, 'user.html', context)


@login_required(login_url='/login/')
def user_parcels_view(request):
    user = request.user
    if is_superuser(user):
        parcels = Parcel.objects.all()
    else:
        parcels = Parcel.objects.filter(recipient=user)
    if parcels is None:
        return HttpResponse(f"Cannot find any parcel for the user {user.username}.")
    context = {'parcels': parcels, 'user': user}
    return render(request, 'parcels_list.html', context)


@login_required(login_url='/login/')
def user_parcel_view(request, parcel_id):
    context = {}
    user = request.user
    if is_superuser(user):
        parcel = Parcel.objects.get(pk=parcel_id)
    else:
        parcel = Parcel.objects.get(recipient=user, pk=parcel_id)
    if parcel is None:
        context['error'] = f"Cannot find a parcel with id {parcel_id} for the user {user.username}."
    context = {'parcel': parcel, 'user': user}
    return render(request, 'parcel.html', context)


@user_passes_test(is_superuser, login_url='/login/')
def user_parcel_update(request, parcel_id):
    parcel = Parcel.objects.get(pk=parcel_id)
    print('parcel', parcel)
    context = {}
    if parcel is None:
        context['error'] = f"Cannot find a parcel with id {parcel_id}."
    if parcel.status:  # Delivered
        return redirect(f'/user/parcels/{parcel_id}')
    old_locker = parcel.post_machine_locker

    if request.method == 'POST':
        # send_date_time = request.POST['send_date_time']
        new_locker_id = request.POST['locker']
        new_locker = Locker.objects.get(pk=new_locker_id)
        print('changes:', new_locker_id)
        # parcel.send_date_time = send_date_time
        parcel.post_machine_locker = new_locker
        parcel.save()
        print('Saved parcel', parcel)

        if new_locker is not None:
            new_locker.status = True  # Loaded
            new_locker.save()
        # in case of move the parcel to a new locker, change the status
        if old_locker is not None and old_locker.id != new_locker_id:
            old_locker.status = False  # Empty
            old_locker.save()

        return redirect('/user/parcels/')

    post_machine = old_locker.post_machine
    lockers = Locker.objects.filter(post_machine=post_machine, status=False) | Locker.objects.filter(id=old_locker.id)
    context = {
        'parcel': parcel,
        'lockers': lockers,
    }
    return render(request, 'parcel_edit.html', context)


@user_passes_test(is_superuser, login_url='/login/')
def user_parcel_create(request):
    if request.method == 'POST':
        print("POST request received")
        sender = request.POST['sender']
        size = request.POST['size']
        send_date_time = request.POST['send_date_time']
        print('New parcel 1:', sender, size, send_date_time)
        users = User.objects.all()
        print(f"Users fetched: {users}")
        post_machines = PostMachine.objects.all()
        print(f"Post machines fetched: {post_machines}")
        context = {
            'sender': sender,
            'size': size,
            'send_date_time': send_date_time,
            'users': users,
            'post_machines': post_machines
        }
        return render(request, 'select_recipient_and_post_machine.html', context)
    return render(request, 'parcel_create.html')


@user_passes_test(is_superuser, login_url='/login/')
def select_recipient_and_post_machine(request):
    # print("Select_recipient view called")
    if request.method == 'POST':
        # print("POST request received")
        sender = request.POST['sender']
        size = request.POST['size']
        send_date_time = request.POST['send_date_time']
        recipient_id = request.POST['recipient']
        post_machine_id = request.POST['post_machine']
        print('New parcel 2:', post_machine_id, recipient_id, sender, size, send_date_time)
        recipient = User.objects.get(pk=recipient_id)
        post_machine = PostMachine.objects.get(pk=post_machine_id)
        if recipient is None or post_machine is None:
            return redirect('/user/parcels/create/')
        print('date time:', send_date_time)
        parcel = Parcel.objects.create(
            sender=sender,
            size=size,
            send_date_time=send_date_time,
            status=True,
            recipient=recipient,
            post_machine=post_machine,
            post_machine_locker=None,
            open_date_time=None
        )
        print('Save new Parcel')
        parcel.save()
        return redirect(f'/user/parcels/')
    return render(request, 'select_recipient_and_post_machine.html')


@user_passes_test(is_superuser, login_url='/login/')
def select_locker(request, parcel_id):
    user = request.user
    if user.is_superuser:
        parcel = Parcel.objects.get(pk=parcel_id)
    else:
        parcel = Parcel.objects.get(recipient=user, pk=parcel_id)
    if parcel is None:
        return HttpResponse(f"Cannot find a parcel {parcel_id} for user {user.username}.", status=404)
    if request.method == 'POST':
        locker_id = request.POST['locker']
        locker = Locker.objects.get(pk=locker_id)
        if locker is None:
            return redirect(f'/user/parcels/{parcel_id}/select_locker/')
        locker.status = True
        locker.save()
        parcel.post_machine_locker = locker
        parcel.save()
        print(f'Locker {locker_id} was Loaded')
        return redirect(f'/user/parcels/')
    recipient = parcel.recipient
    post_machine = parcel.post_machine_recipient
    if recipient is None or post_machine is None:
        return redirect(f'/user/parcels/')
    post_machine_id = post_machine.pk
    lockers = Locker.objects.filter(post_machine_id=post_machine_id, status=False)  # Only show available lockers
    if lockers is None or len(lockers) == 0:
        return redirect(f'/user/parcels/')
    context = {
        'lockers': lockers,
        'parcel_id': parcel.pk,
        'sender': parcel.sender,
        'size': parcel.size,
        'send_date_time': parcel.send_date_time,
        'recipient': parcel.recipient.username,
        'post_machine_id': post_machine_id,
    }
    return render(request, 'select_locker.html', context)


@login_required(login_url='/login/')
def user_get_parcel(request, parcel_id):
    user = request.user
    if user.is_superuser:
        parcel = Parcel.objects.get(pk=parcel_id)
    else:
        parcel = Parcel.objects.get(recipient=user, pk=parcel_id)
    if parcel is None:
        return HttpResponse(f"Cannot find a parcel {parcel_id} for user {user.username}.", status=404)
    if request.method == "POST":
        parcel.status = True  # Delivered
        if parcel.open_date_time is None:
            parcel.open_date_time = timezone.now()
        parcel.save()
        locker = parcel.post_machine_locker
        if locker is None:
            return HttpResponse(f"Linked locker for parcel {parcel_id} not found.", status=400)
        # make the locker empty
        locker.status = False
        print('new parcel status', parcel.status, 'new locker status', locker.status)
        locker.save()
        print('Changes were saved')
        return redirect(f'/user/parcels/{parcel_id}')
    context = {'parcel': parcel, 'user': user}
    return render(request, 'parcel.html', context)
