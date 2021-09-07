from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class KeyChain(models.Model):
    chaincode = models.IntegerField()
    privkey = models.IntegerField()
    pubkey = models.IntegerField()
    fingerprint = models.IntegerField()
    depth = models.IntegerField()
    index = models.IntegerField()
    testnet = models.BooleanField()
    path = models.CharField(max_length=10)

    class Meta:
        ordering = ('index',)

    def __str__(self):
        return self.path


class Account(models.Model):
    keychain = models.ForeignKey(KeyChain,
                                 on_delete=models.CASCADE,
                                 related_name='master_keychain')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='user')
    name = models.CharField(max_length=25)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    index = models.IntegerField()

    class Meta:
        ordering = ('index',)

    def __str__(self):
        return f'Account #{self.index}: {self.name}'

