# Generated by Django 4.0.1 on 2022-09-13 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=10)),
                ('access_no', models.CharField(default='psj62bfdf5d4feb', max_length=16)),
                ('id_no', models.IntegerField(default=0)),
                ('success', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bal.compayuser')),
            ],
        ),
        migrations.CreateModel(
            name='MultiPay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('closing_no', models.IntegerField(default=0)),
                ('access_no', models.CharField(default='abc5580939', max_length=10)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('pay_user', models.ManyToManyField(blank=True, related_name='Collector', to='bal.CompayUser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Giver', to='bal.compayuser')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_no', models.CharField(blank=True, max_length=20)),
                ('recipient_code', models.CharField(blank=True, max_length=20)),
                ('authorization_code', models.CharField(blank=True, max_length=20)),
                ('subscription_code', models.CharField(blank=True, max_length=20)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='bal.compayuser')),
            ],
        ),
    ]