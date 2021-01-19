from django.db import models

# Create your models here.


class employeeTbl(models.Model):
    fname = models.CharField(max_length=100)
    mname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    empid = models.CharField(max_length=10)
    orgName = models.CharField(max_length=200)
    mobno = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    idCard = models.ImageField(null=True,upload_to='photos/')
    regno = models.CharField(primary_key=True, max_length=12)
    regDate = models.DateField()


class loginTbl(models.Model):
    regno = models.ForeignKey(employeeTbl, on_delete=models.CASCADE)
    pwd = models.CharField(max_length=20)


class adminTbl(models.Model):
    uname = models.CharField(max_length=20)
    pwd = models.CharField(max_length=20)


class foodTbl(models.Model):
    item = models.CharField(max_length=100)
    price = models.FloatField()


class bookingTbl(models.Model):
    bookId = models.AutoField(primary_key=True)
    regno = models.ForeignKey(employeeTbl, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    pickTime = models.TimeField(null=True)
    bookDate = models.DateField()


class cartTbl(models.Model):
    bookid = models.ForeignKey(bookingTbl, on_delete=models.CASCADE)
    itemid = models.ForeignKey(foodTbl, on_delete=models.CASCADE)
    count = models.IntegerField()


class billTbl(models.Model):
    bookid = models.ForeignKey(bookingTbl, on_delete=models.CASCADE)
    amt = models.FloatField()
    payment = models.CharField(max_length=50)
