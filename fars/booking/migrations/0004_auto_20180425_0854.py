# Generated by Django 2.0.3 on 2018-04-25 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_bookable_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookable',
            name='icon',
            field=models.CharField(default='tf.svg', max_length=32),
        ),
    ]
