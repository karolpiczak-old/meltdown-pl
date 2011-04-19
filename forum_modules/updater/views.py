from django.http import HttpResponse
from base import generate_installation_key
from settings import SITE_KEY
from forum.views.admin import admin_tools_page, admin_page

@admin_page
def updater_index(request):
    return (
        'modules/updater/index.html',
        {

        },
    )
