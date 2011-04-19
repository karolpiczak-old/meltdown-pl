from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext as _

from views import updater_index

urlpatterns = patterns('',
    url(r'^%s%s$' % (_('admin/'), _('updater/')),  updater_index, name='updater_index'),
)
