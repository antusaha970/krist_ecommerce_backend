# Generated by Django 5.0.6 on 2024-10-26 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('email', models.EmailField(max_length=300)),
                ('message', models.TextField()),
                ('received_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]