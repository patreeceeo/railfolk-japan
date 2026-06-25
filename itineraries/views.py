from django.http import HttpResponse


def home(request):
    return HttpResponse(
        "<h1>Railfolk Japan</h1>"
        "<p>A lightweight site for creating and sharing Japan train and bus itineraries.</p>"
    )
