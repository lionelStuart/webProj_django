from django.shortcuts import render


# Create your views here.

def post_list(request):
    return render(request, 'base.html')


def post_detail(request):
    return render(request, 'base.html')
