# Generated by Django 4.2.7 on 2023-11-04 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_alter_localgorvernment_name_alter_state_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='name',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
