from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import SignUpForm


def home(request):
    return HttpResponse(
        "<h1>Railfolk Japan</h1>"
        "<p>A lightweight site for creating and sharing Japan train and bus itineraries.</p>"
    )


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})
