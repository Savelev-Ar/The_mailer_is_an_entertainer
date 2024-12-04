# Generated by Django 4.2.16 on 2024-12-03 03:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='clients',
            field=models.ManyToManyField(related_name='clients', to='mailing.client', verbose_name='клиенты'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='date_start',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='дата и время первой отправки'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message', to='mailing.message', verbose_name='сообщение'),
        ),
    ]
