from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .avatars import (
    DEFAULT_AVATAR_SVG,
    FALLBACK_CACHE_CONTROL,
    SUCCESS_CACHE_CONTROL,
    SVG_CONTENT_TYPE,
    AvatarFetchError,
    fetch_avatar_svg,
)
from .forms import SignUpForm


def home(request):
    return render(request, "itineraries/index.html")


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


def avatar(request, user_id):
    user = get_object_or_404(get_user_model(), pk=user_id)

    try:
        image = fetch_avatar_svg(user.avatar_key)
        cache_control = SUCCESS_CACHE_CONTROL
    except AvatarFetchError:
        image = DEFAULT_AVATAR_SVG
        cache_control = FALLBACK_CACHE_CONTROL

    response = HttpResponse(image, content_type=SVG_CONTENT_TYPE)
    response["Cache-Control"] = cache_control
    return response
