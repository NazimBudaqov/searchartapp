# Generated by Django 4.2.2 on 2023-07-27 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchartapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yeardata',
            name='country_code_2',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]