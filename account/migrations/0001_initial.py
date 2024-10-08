# Generated by Django 5.0.6 on 2024-07-03 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', models.CharField(default=None, max_length=12, null=True, unique=True)),
                ('profile_picture', models.ImageField(default='profile.jpg', upload_to='account/profile')),
                ('address', models.CharField(default='', max_length=300)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('bio', models.CharField(default='', max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
