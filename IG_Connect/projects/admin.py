# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectDescription)
admin.site.register(ProjectImage)
admin.site.register(ProjectLike)
