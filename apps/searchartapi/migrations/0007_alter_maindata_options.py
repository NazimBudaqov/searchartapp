# Generated by Django 4.2.2 on 2023-08-10 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('searchartapi', '0006_alter_maindata_json_data'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='maindata',
            options={'verbose_name': 'MainData', 'verbose_name_plural': 'MainData'},
        ),
    ]