from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from tables.models import *
import  datetime

# Create your views here.


def home(request):  # homepage code

    for key in list(request.session.keys()):
        if not key.startswith("_"):  # skip keys set by the django system
            del request.session[key]

    if request.method=='POST':
        regno = request.POST['username']
        pwd = request.POST['password']

        obj = adminTbl.objects.filter(uname=regno, pwd=pwd)
        if obj.count()>0:
            request.session['regno'] = 0
            return redirect("http://127.0.0.1:8000/cafeAdmin")

        obj = loginTbl.objects.filter(regno=regno, pwd=pwd)
        if obj.count()>0:
            request.session['regno'] = regno
            return redirect("http://127.0.0.1:8000/employee")
        else:
            messages.success(request, 'Invalid Register No. / Password')

    return render(request, 'home/index.html')


def reg(request):   # employee registration

    if request.method=='POST' and request.FILES['idCard']:
        fname = request.POST['fname']
        mname = request.POST['mname']
        lname = request.POST['lname']
        empid = request.POST['empid']
        orgName = request.POST['orgName']
        mobno = request.POST['mobno']
        email = request.POST['email']
        idCard = request.FILES.get('idCard')
        pwd = request.POST['pwd1']
        regDate = datetime.date.today()

        obj = employeeTbl.objects.all()
        regno = str(empid) + str(obj.count()+1)

        obj = employeeTbl.objects.filter(empid=empid)
        obj1 = employeeTbl.objects.filter(email=email)
        if obj.count()>0 or obj1.count()>0:
            messages.success(request, 'Employee Details Exists')
            return render(request, 'home/registration.html')

        dbObj = employeeTbl(fname=fname, mname=mname, lname=lname, empid=empid, orgName=orgName, mobno=mobno, email=email, idCard=idCard, regno=regno, regDate=regDate)
        dbObj.save()

        dbObj = loginTbl(regno=dbObj, pwd=pwd)
        dbObj.save()


        obj = employeeTbl.objects.filter(empid=empid)
        request.session['id'] = empid
        return redirect('http://127.0.0.1:8000/home/preview/')

    return render(request, 'home/registration.html')

def previewEmp(request):
    if 'id' in list(request.session.keys()):
        empid = request.session['id']
        obj = employeeTbl.objects.filter(empid=empid)
        return render(request, 'home/preview.html', {'obj': obj[0]})
    return render(request, 'home/preview.html')

def validate_register(request):
    email = request.GET.get('email')
    empid = request.GET.get('empid')
    s = employeeTbl.objects.filter(empid=empid)
    s1 = employeeTbl.objects.filter(email=email)

    email_status = False
    empid_status = False
    if s.count() > 0:
        empid_status = True
    if s1.count() > 0:
        email_status = True
    data = {
        'email_status': email_status,
        'empid_status': empid_status
    }
    return JsonResponse(data)