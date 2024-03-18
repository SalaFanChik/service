from django.contrib import admin
from .models import User, ClientProfile, StaffProfile, Order, Service, WorkingHours

admin.site.register(User)
admin.site.register(ClientProfile)
admin.site.register(StaffProfile)
admin.site.register(Order)
admin.site.register(Service)
admin.site.register(WorkingHours)
