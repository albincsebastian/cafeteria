from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from tables.models import *
import  datetime


# Create your views here.

def home(request):  # employee homepage
    keys = request.session.keys()
    if 'regno' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home')

    regno = request.session['regno']
    obj = employeeTbl.objects.filter(regno=regno)
    return render(request, 'employee/master.html', {'obj': obj})

def booking(request):   # book food
    keys = request.session.keys()
    if 'regno' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home')


    regno = request.session['regno']

    obj = foodTbl.objects.all()
    if obj.count()==0:
      messages.success(request, 'Food Items Empty')
      return redirect('http://127.0.0.1:8000/employee')

    obj1 = bookingTbl.objects.filter(regno_id=regno, status=0)
    if obj1.count()>0:
      messages.success(request, 'Already made a Booking. Please Complete Billing')
      return redirect('http://127.0.0.1:8000/employee/billing/')

    obj1 = bookingTbl.objects.filter(regno_id=regno, status=1)
    if obj1.count() > 0:
        messages.success(request, 'Already made a Booking')
        return redirect('http://127.0.0.1:8000/employee')

    if request.method == 'POST':
        print(request.POST)
        items = []
        count = []
        for key in list(request.POST.keys()):
            if key.startswith("items"):
                items.append(request.POST[key])
                num = 'count' + str(key[5:])
                count.append(request.POST[num])

        pickTime = request.POST['pickTime']

        if len(items) == 0:
            messages.success(request, 'Pick Atleast One Item')
            return redirect('http://127.0.0.1:8000/employee/booking')

        obj1 = employeeTbl.objects.filter(regno=request.session['regno'])
        if pickTime:
            db = bookingTbl(regno=obj1[0], status=0, bookDate=datetime.date.today(), pickTime=pickTime)
        else:
            db = bookingTbl(regno=obj1[0], status=0, bookDate=datetime.date.today())
        db.save()

        for i in range(len(items)):
            obj1 = foodTbl.objects.filter(id=items[i])
            db1 = cartTbl(bookid=db, itemid=obj1[0], count=count[i])
            db1.save()

        messages.success(request, 'Booking Success')
        return redirect('http://127.0.0.1:8000/employee/billing/')

    return render(request, 'employee/booking.html', {'obj': obj})


def rate(request):   # rate of items in cafe
    keys = request.session.keys()
    if 'regno' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home')

    obj = foodTbl.objects.all()
    if obj.count()==0:
      messages.success(request, 'Food Items Empty')
      return redirect('http://127.0.0.1:8000/employee')

    return render(request, 'employee/rate.html', {'obj': obj})


def billing(request):
    keys = request.session.keys()
    if 'regno' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home')

    regno = request.session['regno']

    obj = bookingTbl.objects.filter(regno_id=regno, status=0)
    if obj.count() == 0:
        messages.success(request, 'Pending Bills Not Found')
        return redirect('http://127.0.0.1:8000/employee')

    c = cartTbl.objects.filter(bookid=obj[0])
    amt = 0
    for i in c:
        amt += i.itemid.price * i.count

    if request.method == 'POST':
        payment = request.POST['payment']
        bookid = obj[0]

        db = billTbl(bookid=bookid, amt=amt, payment=payment)
        db.save()

        db = bookingTbl.objects.filter(bookId=obj[0].bookId).update(status=1)
        messages.success(request, 'Payment Success')
        return redirect('http://127.0.0.1:8000/employee')

    return render(request, 'employee/billing.html', {'obj': obj, 'amt': amt})

