from django.shortcuts import render


def landing_page(request):
    # context = {'user': request.user}
    return render(request, 'landing_page.html')
