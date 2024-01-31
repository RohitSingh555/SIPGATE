from django.db import models

class SipgateUser(models.Model):
    sipgate_user = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    alias_name = models.CharField(max_length=255)
    sipgate_user_token = models.CharField(max_length=255)

class CallLogs(models.Model):
    sipgate_user = models.ForeignKey(SipgateUser, on_delete=models.CASCADE)
    called_on = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    date = models.DateTimeField(null=True, blank=True)
    call_type = models.BooleanField(default=False)

class CompanyContacts(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    sipgate_user = models.ForeignKey(SipgateUser, on_delete=models.CASCADE)

class Call(models.Model):
    event = models.CharField(max_length=255)
    from_number = models.CharField(max_length=15)
    to_number = models.CharField(max_length=15)
    direction = models.CharField(max_length=10,null=True, blank=True)
    call_id = models.CharField(max_length=255, null=True, blank=True)
    user = models.CharField(max_length=255)
    user_id_list = models.CharField(max_length=255)
    user_id_list1 = models.CharField(max_length=255)  
    full_user_id_list = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        super(Call, self).save(*args, **kwargs)