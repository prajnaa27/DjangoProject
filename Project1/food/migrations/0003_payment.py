# Generated by Django 4.2 on 2025-06-06 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_contactmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=200, unique=True)),
                ('payment_id', models.CharField(blank=True, max_length=200, null=True)),
                ('amount', models.IntegerField(help_text='Amount in paise ex:Rs 50 = 5000')),
                ('status', models.CharField(choices=[('created', 'Created'), ('paid', 'Paid'), ('failed', 'Failed')], default='created', max_length=200)),
                ('customer_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
