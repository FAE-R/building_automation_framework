# Importing the Django admin module, which provides a built-in interface for managing the site.
from django.contrib import admin

# Importing all models from the agents.models module.
from agents.models import *


# Registering the Profile model with the Django admin site so that it can be managed through the admin interface.
admin.site.register(Profile)

# Registering the Building model with the Django admin site so that it can be managed through the admin interface.
admin.site.register(Building)

# Registering the Room model with the Django admin site so that it can be managed through the admin interface.
admin.site.register(Room)

