# Generated by Django 4.2.13 on 2024-08-06 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ATM_MGNT', '0003_alter_atmdown_down_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atmdown',
            name='atm_brand',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='atmdown',
            name='down_reason',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ATM_MGNT.downreason'),
        ),
    ]