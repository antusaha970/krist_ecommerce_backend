# Generated by Django 5.0.6 on 2024-07-03 15:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_account_options_remove_account_bio_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountPasswordResetProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reset_password_otp', models.IntegerField(blank=True, default=None, null=True)),
                ('reset_password_expire', models.DateTimeField(blank=True, default=None, null=True)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ResetPassword', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]