# coding: utf-8

from django.core.management.base import BaseCommand
from forum.models import Node

import logging

class Command(BaseCommand):

    def handle(self,*args, **options):
        # Re-render node bodies
        nodes = Node.objects.all()
        for node in nodes:
            try:
                node.body = node.rendered(node.body)
                node.save()
                print node.body
            except Exception, e:
                logging.error(e)
