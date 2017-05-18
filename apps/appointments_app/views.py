from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from datetime import date
from .models import User, Appointment
# Create your views here.


def index(request):
    return render(request, 'appointments_app/index.html')

def register(request):
    if request.method == 'GET':
        return redirect ('/')
    newuser = User.objects.validate(request.POST)
    print newuser
    if newuser[0] == False:
        for each in newuser[1]:
            messages.error(request, each) #for each error in the list, make a message for each one.
        return redirect('/')
    if newuser[0] == True:
        messages.success(request, 'Well done')
        request.session['id'] = newuser[1].id
        return redirect('/appoint')

def login(request):
    if 'id' in request.session:
        return redirect('/appoint')
    if request.method == 'GET':
        return redirect('/')
    else:
        user = User.objects.login(request.POST)
        print user
        if user[0] == False:
            for each in user[1]:
                messages.add_message(request, messages.INFO, each)
            return redirect('/')
        if user[0] == True:
            messages.add_message(request, messages.INFO,'Welcome, You are logged in!')
            request.session['id'] = user[1].id
            return redirect('/appoint')


def appoint(request):
    if 'id' not in request.session:
        return redirect ("/")
    appointments= Appointment.objects.filter(user__id=request.session['id']).exclude(date=date.today())
    user= User.objects.get(id=request.session['id'])
    # others = User.objects.all().exclude(appoint__id=request.session['id'])
    context = {
        "user": user,
        'time': date.today(),
        "appointments": appointments,
        "today_appoint":  Appointment.objects.filter(user__id = request.session['id']).filter(date = date.today())
    }
    return render(request, 'appointments_app/appointment.html', context)


def update(request, appoint_id):
    try:
        appointment= Appointment.objects.get(id=appoint_id)
    except Appointment.DoesNotExist:
        messages.info(request,"appointment Not Found")
        return redirect('/appoint')

    context={
        "appointment": appointment,
        # "others": User.objects.filter(joiner__id=appoint.id).exclude(id=appoint.creator.id),
    }
    return render(request, 'appointments_app/updatetime.html', context)

def edit_appoint(request, appoint_id):
    if 'id' not in request.session:
        return redirect ('/')
    if request.method != 'POST':
        messages.info(request, "Cannot edit like this!")
        return redirect('/update'+ appoint_id)

    try:
        print("/"*50)
        update_app = Appointment.objects.edit_appointment(request.POST, appoint_id)
        print "got to edit_appoint Try"
    except Appointment.DoesNotExist:
        messages.info(request,"appointment Not Found")
        return redirect('/update/'+appoint_id)
    if update_app[0]==False:
        messages.info(request, "Please fill in all the spaces and make sure it's valid!")
        return redirect('/update/'+appoint_id)
    else:
        messages.success(request, "successfuly updated information")
        return redirect('/appoint')

def add(request):
    if request.method != "POST":
        messages.error(request,"Can't add like that!")
        return redirect('/')
    else:
        add_appoint= Appointment.objects.appointval(request.POST, request.session['id'])
        if add_appoint[0] == False:
            for each in add_appoint[1]:
                messages.error(request, each) #for each error in the list, make a message for each one.
            return redirect('/appoint')
        if add_appoint[0] == True:
            messages.success(request, 'Appointment Successfully Added')
            return redirect('/appoint')
#
def delete(request, appoint_id):
    try:
        target= Appointment.objects.get(id=appoint_id)
    except Appointment.DoesNotExist:
        messages.info(request,"Message Not Found")
        return redirect('/appoint')
    target.delete()
    return redirect('/appoint')
# #

def logout(request):
    if 'id' not in request.session:
        return redirect('/')
    print "*******"
    print request.session['id']
    del request.session['id']
    return redirect('/')
