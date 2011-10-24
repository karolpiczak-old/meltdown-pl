from base import Setting, SettingSet
from django.utils.translation import ugettext_lazy as _

""" view settings """
VIEW_SET = SettingSet('view', _('View settings'), _("Set up how certain parts of the site are displayed."), 20)

EMBED_YOUTUBE_VIDEOS = Setting('EMBED_YOUTUBE_VIDEOS', True, VIEW_SET, dict(
label = _("Embed YouTube Videos"),
help_text = _("If you check this YouTube videos will be embedded"),
required=False))

SHOW_LATEST_COMMENTS_FIRST = Setting('SHOW_LATEST_COMMENTS_FIRST', False, VIEW_SET, dict(
label = _("Show latest comments first"),
help_text = _("Choose this if you want the latest comments to appear first."),
required=False))


SUMMARY_LENGTH = Setting('SUMMARY_LENGTH', 300, VIEW_SET, dict(
label = _("Summary Length"),
help_text = _("The number of characters that are going to be displayed in order to get the content summary.")))

# Tag settings
RECENT_TAGS_SIZE = Setting('RECENT_TAGS_SIZE', 25, VIEW_SET, dict(
label = _("Recent tags block size"),
help_text = _("The number of tags to display in the recent tags block in the front page.")))

SHOW_TAGS_IN_A_CLOUD = Setting('SHOW_TAGS_IN_A_CLOUD', True, VIEW_SET, dict(
label = _("Show tags in a cloud"),
help_text = _("If selected the tags in the recent tags widget will be displayed in a cloud."),
required=False))

TAGS_CLOUD_MIN_OCCURS = Setting('TAGS_CLOUD_MIN_OCCURS', 1, VIEW_SET, dict(
label = _("Tags cloud min occurs"),
help_text = _("Used to calculate the font size of the tags in the cloud widget.")))

TAGS_CLOUD_MAX_OCCURS = Setting('TAGS_CLOUD_MAX_OCCURS', 35, VIEW_SET, dict(
label = _("Tags cloud max occurs"),
help_text = _("Used to calculate the font size of the tags in the cloud widget.")))

TAGS_CLOUD_MIN_FONT_SIZE = Setting('TAGS_CLOUD_MIN_FONT_SIZE', 10, VIEW_SET, dict(
label = _("Tags cloud min font size"),
help_text = _("Used to calculate the font size of the tags in the cloud widget.")))

TAGS_CLOUD_MAX_FONT_SIZE = Setting('TAGS_CLOUD_MAX_FONT_SIZE', 25, VIEW_SET, dict(
label = _("Tags cloud max font size"),
help_text = _("Used to calculate the font size of the tags in the cloud widget.")))

RECENT_AWARD_SIZE = Setting('RECENT_AWARD_SIZE', 15, VIEW_SET, dict(
label = _("Recent awards block size"),
help_text = _("The number of awards to display in the recent awards block in the front page.")))

UPDATE_LATEST_ACTIVITY_ON_TAG_EDIT = Setting('UPDATE_LATEST_ACTIVITY_ON_TAG_EDIT', True, VIEW_SET, dict(
label = _("Update latest activity on tag edit"), required=False,
help_text = _("If you check this the latest activity will be updated when editing only the tags of a question.")))

LIMIT_RELATED_TAGS = Setting('LIMIT_RELATED_TAGS', 0, VIEW_SET, dict(
label = _("Limit related tags block"),
help_text = _("Limit related tags block size in questions list pages. Set to 0 to display all all tags.")))

