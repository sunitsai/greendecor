from __future__ import unicode_literals

from django.apps import AppConfig
from django.contrib import algoliasearch
from .index import *

class CoreConfig(AppConfig):
    name = 'core'
    def ready(self):
        Plants = self.get_model('Plants')
        Category = self.get_model('Category')
        algoliasearch.register(Plants,PlantsIndex)
        algoliasearch.register(Category,CategoryIndex)
