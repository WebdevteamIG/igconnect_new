import os
import re
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IG_Connect.settings')

import django
django.setup()

from events.models import Event, EventRegisterationRequest
from authentication.models import Userprofile

event = Event.objects.get(name = "Arduino Workshop")

reqs = EventRegisterationRequest.objects.filter(event = event, status = 3)

for req in reqs:
	print req.user
	profile = Userprofile.objects.get(user = req.user)
	profile.isApproved = True
	profile.save()




