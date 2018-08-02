# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Event)
admin.site.register(EventQuestion)
admin.site.register(EventRegisterationRequest)
admin.site.register(EventQuestionResponse)
