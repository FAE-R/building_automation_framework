
import os
import django
from channels.routing import get_default_application
from channels.layers import get_channel_layer

# Setting the default settings module for the 'ba_framework' project.
# This environment variable tells Django which settings file to use.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ba_framework.settings")

django.setup()
application = get_default_application()
channel_layer = get_channel_layer()
