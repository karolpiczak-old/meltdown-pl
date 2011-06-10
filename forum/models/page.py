from base import *
from django.utils.translation import ugettext as _

def silent_permalink(func):
    """
    Decorator that calls urlresolvers.reverse() to return a URL using
    parameters returned by the decorated function "func".

    "func" should be a function that returns a tuple in one of the
    following formats:
        (viewname, viewargs)
        (viewname, viewargs, viewkwargs)
    """
    from django.core.urlresolvers import reverse
    def inner(*args, **kwargs):
        bits = func(*args, **kwargs)
        try:
            return reverse(bits[0], None, *bits[1:3])
        except:
            return "javascript:alert('Configure this page URL in the urls.py file');"
    return inner

class Page(Node):
    friendly_name = _("page")

    @property
    def published(self):
        return self.marked

    @property
    def html(self):
        return self._as_markdown(self.body)

    def save(self, *args, **kwargs):
        old_options = self._original_state.get('extra', None)

        super(Page, self).save(*args, **kwargs)

        registry = settings.STATIC_PAGE_REGISTRY

        if old_options:
            registry.pop(old_options.get('path', ''), None)

        registry[self.extra['path']] = self.id


        settings.STATIC_PAGE_REGISTRY.set_value(registry)

    @property
    def headline(self):
        if self.published:
            return self.title
        else:
            return _("[Unpublished] %s") % self.title

    @silent_permalink
    def get_absolute_url(self):
        return ('static_page', (), {'path': self.extra['path']})
        
    def activate_revision(self, user, revision, extensions=['urlize']):
        self.title = revision.title
        self.tagnames = revision.tagnames        
        self.body = revision.body

        self.active_revision = revision
        self.update_last_activity(user)

        self.save()

    class Meta(Node.Meta):
        proxy = True

    
