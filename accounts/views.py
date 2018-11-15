from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from accounts.forms import UserEditForm, UserProfileEditForm, UserRegistrationForm
from accounts.models import UserProfile


@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            '''
            create empty profile so as to edit
            '''
            profile = UserProfile.objects.create(user=new_user)
            return render(request,
                          'accounts/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        """
        ???
        """
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = UserProfileEditForm(instance=request.user.userprofile,
                                           data=request.POST,
                                           files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)
    return render(request,
                  'accounts/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
