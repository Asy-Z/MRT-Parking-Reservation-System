from django.core.management.base import BaseCommand
from MRT_Webapp.models import Reservation, Parking, Payment

class Command(BaseCommand):
    help = 'Clear all reservations and reset parking statuses'

    def handle(self, *args, **options):
        # Clear all reservations
        Reservation.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all reservations.'))
        
        Payment.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all reservations.'))

        # Reset parking status to 'Available'
        Parking.objects.update(Status='Available')
        self.stdout.write(self.style.SUCCESS('Successfully reset all parking statuses to Available.'))
        
