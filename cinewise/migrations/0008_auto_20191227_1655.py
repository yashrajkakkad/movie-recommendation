# Generated by Django 2.2.7 on 2019-12-27 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinewise', '0007_auto_20191121_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinput',
            name='nodes',
            field=models.ManyToManyField(blank=True, null=True, to='cinewise.Node'),
        ),
    ]