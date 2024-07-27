from django.core.management.base import BaseCommand
from accounts import models
from datetime import datetime, timedelta
import pytz


# class name must be command
class Command(BaseCommand):
    # help is required
    help = 'remove all expired codes'
    # must write handle
    def handle(self, *args, **options):
        expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=2)
        # __lt = smallest code
        models.OtpCode.objects.filter(created__lt=expired_time).delete()
        self.stdout.write('all expired otp codes removed')