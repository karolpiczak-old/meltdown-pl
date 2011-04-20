import sys

from django import VERSION as DJANGO_VERSION
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.utils import simplejson

from base import get_site_views, get_server_name
from settings import SITE_KEY
from forum.settings import APP_URL, SVN_REVISION
from forum.views.admin import admin_tools_page, admin_page

@admin_tools_page(_('updater'), _('Update Checker'))
def updater_index(request):
    return (
        'modules/updater/index.html',
        {

        },
    )

def updater_check(request):
    # Get the SVN Revision
    try:
        svn_revision = int(SVN_REVISION.replace('SVN-', ''))
    except ValueError:
        # Here we'll have to find another way of getting the SVN revision
        svn_revision = 0

    statistics = """<check>
    <key value="%(site_key)s" />
    <app_url value="%(app_url)s" />
    <svn_revision value="%(svn_revision)d" />
    <views value="%(site_views)d" />
    <active_users value="11959" />
    <server value="%(server_name)s" />
    <python_version value="%(python_version)s" />
    <django_version value="%(django_version)s" />
    <database value="MySQL 5" />
    <os value="Linux" />
</check> """ % {
        'site_key' : SITE_KEY,
        'app_url' : APP_URL,
        'svn_revision' : svn_revision,
        'site_views' : get_site_views(),
        'server_name' : get_server_name(),
        'python_version' : ''.join(sys.version.splitlines()),
        'django_version' : str(DJANGO_VERSION),
    }
    return HttpResponse(statistics, mimetype='text/plain')


    json = simplejson.dumps({'name' : 'Jordan'})
    return HttpResponse(json, mimetype='application/json')