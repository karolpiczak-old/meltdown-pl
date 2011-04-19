from django.http import HttpResponse
from base import generate_installation_key
from settings import SITE_KEY

def updater_index(request):
    return HttpResponse(str(SITE_KEY))
