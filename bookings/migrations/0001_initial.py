# Generated by Django 5.1.7 on 2025-03-15 22:26

import bookings.models
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('properties', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
                ('status', models.CharField(choices=[('payment_pending', 'Payment pending'), ('paid', 'Paid'), ('canceled', 'Canceled')], default='payment_pending', max_length=50)),
                ('payment_intent_id', models.CharField(blank=True, max_length=255)),
                ('payment_expiration_time', models.DateTimeField(blank=True, null=True)),
                ('reference_code', models.CharField(default=bookings.models.generate_reference_code, max_length=6)),
                ('property', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='properties.property')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
    ]
