# Generated by Django 3.1 on 2021-01-16 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='bookingTbl',
            fields=[
                ('bookId', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.IntegerField(default=0)),
                ('pickTime', models.TimeField()),
                ('bookDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='employeeTbl',
            fields=[
                ('fname', models.CharField(max_length=100)),
                ('mname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=100)),
                ('empid', models.IntegerField()),
                ('orgName', models.CharField(max_length=200)),
                ('mobno', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=100)),
                ('idCard', models.ImageField(null=True, upload_to='photos/')),
                ('regno', models.IntegerField(primary_key=True, serialize=False)),
                ('regDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='foodTbl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=100)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='loginTbl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pwd', models.CharField(max_length=20)),
                ('regno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.employeetbl')),
            ],
        ),
        migrations.CreateModel(
            name='cartTbl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('bookid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.bookingtbl')),
                ('itemid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.foodtbl')),
            ],
        ),
        migrations.AddField(
            model_name='bookingtbl',
            name='regno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.employeetbl'),
        ),
        migrations.CreateModel(
            name='billTbl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amt', models.FloatField()),
                ('payment', models.CharField(max_length=50)),
                ('bookid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.bookingtbl')),
            ],
        ),
    ]