from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from keychain.models import KeyChain

class Account(models.Model):
    keychain = models.ForeighKey(KeyChain, on_delete=models.CASCADE, related_name='nuit_keychain')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nuit_account')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('index',)

    def __str__(self):
        return self.path

