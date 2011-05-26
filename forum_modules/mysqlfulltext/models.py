from django.db import models

class MysqlFtsIndex(models.Model):
    node       = models.OneToOneField('Node', related_name='ftsindex')
    body       = models.TextField()
    title      = models.CharField(max_length=300)
    tagnames   = models.CharField(max_length=255)

    class Meta:
        managed = False
        app_label = 'forum'