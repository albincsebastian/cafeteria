# Generated by Django 3.1 on 2021-01-16 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0002_auto_20210116_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeetbl',
            name='regno',
            field=models.CharField(max_length=12, primary_key=True, serialize=False),
        ),
    ]