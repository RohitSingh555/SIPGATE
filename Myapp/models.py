from django.db import models
from django.utils import timezone

class SipgateUser(models.Model):
    sipgate_user = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    caller = models.CharField(max_length=255, null=True)
    alias_name = models.CharField(max_length=255)
    sipgate_user_token = models.CharField(max_length=255)

class Devices(models.Model):
    device_id = models.CharField(max_length=255, null=True)
    caller_id = models.CharField(max_length=255, null=True)
    sipgate_user = models.ForeignKey(SipgateUser, on_delete=models.CASCADE)

class CompanyContact(models.Model):  
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

class CallLog(models.Model):
    device = models.ForeignKey(Devices, on_delete=models.CASCADE, default=None)
    called_on_number = models.CharField(max_length=255, null=True, blank=True)
    duration = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    call_type = models.BooleanField(default=False)
    caller = models.CharField(max_length=255, null=True, blank=True)
    caller_id = models.CharField(max_length=255, null=True, blank=True)


class Call(models.Model):
    event = models.CharField(max_length=255, null=True)
    from_number = models.CharField(max_length=15, null=True)
    to_number = models.CharField(max_length=15, null=True)
    direction = models.CharField(max_length=10, null=True, blank=True)
    call_id = models.CharField(max_length=255, null=True)
    user = models.CharField(max_length=255, null=True)
    user_id_list = models.CharField(max_length=255, null=True)
    user_id_list1 = models.CharField(max_length=255, null=True)  
    full_user_id_list = models.CharField(max_length=255, null=True)

    def save(self, *args, **kwargs):
        super(Call, self).save(*args, **kwargs)
