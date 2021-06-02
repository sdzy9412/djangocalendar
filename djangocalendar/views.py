from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from calendar_app.forms import signInForm
from django.contrib.auth.forms import UserCreationForm


def signin(request):
    forms = signInForm()
    if request.method == 'POST':
        forms = signInForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('calendarapp:calendar')
    context = {'form': forms}
    return render(request, 'signin.html', context)


def user_logout(request):
    logout(request)
    return redirect('signin')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('calendarapp:calendar')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
