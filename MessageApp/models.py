from django.db import models


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    objects = models.Manager()


class Messages(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(Users, related_name='sender', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Users, related_name='recipient', on_delete=models.CASCADE)
    message = models.CharField(max_length=1200)
    subject = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp', )
