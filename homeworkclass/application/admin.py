from django.contrib import admin
from .models import *

admin.site.register([Grade, SchoolClass, SchoolHomework, UserClass])
