from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(SipgateUser)
admin.site.register(CallLogs)
admin.site.register(CompanyContacts)