# Generated by Django 4.2.2 on 2023-06-30 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('searchartapi', '0004_yeardata_indicator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subsector',
            name='sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subsectors', to='searchartapi.sector'),
        ),
    ]
