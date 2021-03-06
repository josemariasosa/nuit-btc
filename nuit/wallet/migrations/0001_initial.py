# Generated by Django 3.2.7 on 2021-09-07 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyChain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chaincode', models.IntegerField()),
                ('privkey', models.IntegerField()),
                ('pubkey', models.IntegerField()),
                ('fingerprint', models.IntegerField()),
                ('depth', models.IntegerField()),
                ('index', models.IntegerField()),
                ('testnet', models.BooleanField()),
                ('path', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ('index',),
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('index', models.IntegerField()),
                ('keychain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='master_keychain', to='wallet.keychain')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('index',),
            },
        ),
    ]
