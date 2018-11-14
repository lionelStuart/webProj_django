from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def register(request):

    return render(request, 'accounts/register.html')
