from django.contrib import admin
from pay.models import *

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Discount)
admin.site.register(Tax)
