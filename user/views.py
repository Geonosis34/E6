from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import UpdateUserForm, UpdateProfileForm, SignUpForm
# from chat.forms import SignUpForm
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    user.profile.is_online = True
    user.profile.save()


@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    user.profile.is_online = False
    user.profile.save()


def index(request):
    if request.user.is_authenticated:
        user.profile.is_online = True
        user.profile.save()
        return redirect('main')
    if request.method == 'GET':
        return render(request, 'user/login.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            user.profile.is_online = True
            user.profile.save()

        else:
            return HttpResponse('{"error": "Пользователь не найден"}')
        return redirect('main')


def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('profile')

    else:
        print("www")
        form = SignUpForm()
    template = 'user/register.html'
    context = {'form': form}
    return render(request, template, context)


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлен')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
        chats = request.user.profile.get_chats

    return render(request, 'user/profile.html', {'user_form': user_form, 'profile_form': profile_form, 'chats': chats})
