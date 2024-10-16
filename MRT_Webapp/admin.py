from django.contrib import admin

from .models import User, Commuter, Administrator, Payment, Reservation, Parking

admin.site.register(User)
admin.site.register(Commuter)
admin.site.register(Administrator)
admin.site.register(Payment)
admin.site.register(Reservation)
admin.site.register(Parking)