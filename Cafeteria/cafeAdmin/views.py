from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from tables.models import *
import  datetime


# Create your views here.

def home(request):  # cafeAdmin homepage
    keys = request.session.keys()
    if 'regno' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home')
    return render(request, 'cafeAdmin/master.html')


def addItems(request):  # add food items
    keys = request.session.keys()
    if 'regno' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home')

    if request.method=='POST':
        item = request.POST['item']
        price = request.POST['price']

        obj = foodTbl(item=item, price=price)
        obj.save()
        messages.success(request, 'Food Item Saved')

    return render(request, 'cafeAdmin/addItems.html')


def changeRate(request):  # modify price of foods
    keys = request.session.keys()
    if 'regno' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home')


    if request.method=='POST':
        id = request.POST['item']
        price = request.POST['price']
        obj = foodTbl.objects.filter(id=id).update(price=price)
        messages.success(request, 'Rate Modified')

    obj = foodTbl.objects.all()
    if obj.count() == 0:
        messages.success(request, 'Food List is Empty')
        return redirect("http://127.0.0.1:8000/cafeAdmin")

    return render(request, 'cafeAdmin/changeRate.html',{'obj': obj})


def orders(request):  # make confirmation for orders

    book = bookingTbl.objects.filter(status=1)
    if book.count()==0:
        messages.success(request, 'Pending Orders Not Found')
        return redirect("http://127.0.0.1:8000/cafeAdmin")

    if request.method == 'POST':
        if 'details' in list(request.POST.keys()):
            regno = request.POST['regno']
            obj = bookingTbl.objects.filter(regno_id=regno, status=1)
            bill = billTbl.objects.filter(bookid=obj[0])
            cart = cartTbl.objects.all()
            return render(request, 'cafeAdmin/orders.html', {'obj': obj, 'bill': bill, 'cart': cart,'bookid': obj[0]})

        if 'formSubmit' in list(request.POST.keys()):
            bookNo = request.POST['bookNo']
            obj = bookingTbl.objects.filter(bookId=bookNo).update(status=2)
            book = bookingTbl.objects.filter(status=1)
            if book.count() == 0:
                return redirect("http://127.0.0.1:8000/cafeAdmin")

        if 'cancel' in list(request.POST.keys()):
            bookNo = request.POST['bookNo']
            obj = bookingTbl.objects.filter(bookId=bookNo).update(status=3)

            book = bookingTbl.objects.filter(status=1)
            if book.count() == 0:
                return redirect("http://127.0.0.1:8000/cafeAdmin")

    return render(request, 'cafeAdmin/orders.html', {'book': book})


def rate(request):   # rate of items in cafe
    keys = request.session.keys()
    if 'regno' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home')

    obj = foodTbl.objects.all()
    if obj.count()==0:
      messages.success(request, 'Food Items Empty')
      return redirect('http://127.0.0.1:8000/cafeAdmin')

    return render(request, 'cafeAdmin/rate.html', {'obj': obj})