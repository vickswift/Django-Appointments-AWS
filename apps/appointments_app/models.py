from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime
from django.utils import timezone
import re
import bcrypt

Name_Regex = re.compile(r'^[A-Za-z ]+$')

# Create your models here.
class userManager(models.Manager):
    def validate (self, postData):
        errors = []
        if len(postData['name']) < 2:
            errors.append("Name needs to be more than 1 letter")
        if not Name_Regex.match(postData['name']):
            errors.append("name can only be letters")
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors.append("email already exists")
        if len(postData["email"])==0:
            errors.append("Please insert an email address in the bracket")
        elif not re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$', postData["email"]):
            errors.append("Please insert a valid email address")
        if postData['password'] != postData['confirm_password']:
            errors.append("Your passwords don't match")
        if len(postData['password']) < 8:
            errors.append("Password needs to be more than 8 letters")
        if str(date.today()) < str(postData['dob']):
            errors.append("Please input a valid Date. Note: DOB cannot be in the future.")
        if len(errors) == 0:
            #create the user
            newuser = User.objects.create(name= postData['name'], email= postData['email'], dob= postData['dob'], password= bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
            return (True, newuser)
        else:
            return (False, errors)

    def login(self, postData):
        errors = []
        if 'email' in postData and 'password' in postData:
            try:
                print 50*('8')
                user = User.objects.get(email = postData['email'])#userManage acceses the database using .get (finds that one user's object)
            except User.DoesNotExist: #if the user doesnt exist from the .get(.get returns nothin, this 'except' prevents an error message)
                print 50*('4')
                errors.append("Sorry, please try logging in again")
                return (False, errors)
        #password field/check
        pw_match = bcrypt.hashpw(postData['password'].encode(), user.password.encode())
        print 10*"3", user.password
        if pw_match == user.password:
            return (True, user)
        else:
            errors1.append("Sorry please try again!!!!")
            return (False, errors)

    # def addfriend(self, id, friend_id):
    #     if len(User.objects.filter(friends=friend_id, id=id))>0:
    #         return {'errors':'You already added this friend'}
    #     else:
    #         adder = self.get(id=id)
    #         addfriend= self.get(id = friend_id)
    #         addfriend.friends.add(adder)
    #         return {}
    #
    # def removefriend(self, id, friend_id):
    #     if len(User.objects.filter(friends=friend_id, id=id))==0:
    #         return {'errors':'You have already removed this friend before'}
    #     else:
    #         removeuser= self.get(id=id)
    #         removefriend= self.get(id=friend_id)
    #         removeuser.friends.remove(removefriend)
    #         print removeuser , removefriend
    #         return {}

class User(models.Model):
    name = models.CharField(max_length=45)
    password = models.CharField(max_length=100)
    email= models.CharField(max_length=45, blank=True, null=True)
    dob= models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()

class appointManager(models.Manager):
    def appointval(self, postData, id):
        errors = []
        # print str(datetime.today()).split()[1]-> to see just the time in datetime
        print postData["time"]
        print datetime.now().strftime("%H:%M")
        if postData['date']:
            if not postData["date"] >= unicode(date.today()):
                errors.append("Date must be set in future!")
            if len(postData["date"]) < 1:
                errors.append("Date field can not be empty")
            print "got to appointment post Data:", postData['date']
        if len(Appointment.objects.filter(date = postData['date'] ,time= postData['time'])) > 0:
            errors.append("Can Not create an appointment on existing date and time")
        if len(postData['task'])<2:
            errors.append("Please insert take, must be more than 2 characters")
        if len(errors)==0:
            makeappoint= Appointment.objects.create(user=User.objects.get(id=id), task= postData['task'],date= str(postData['date']),time= postData['time'])
            return(True, makeappoint)
        else:
            return(False, errors)

    def edit_appointment(self, postData, app_id):
        errors = []
        print errors
        # if postData['edit_date']:
        if not postData["edit_date"] >= unicode(date.today()):
            errors.append("Appointment date can't be in the past!")
            print "appoint date can't be past"
        if postData["edit_date"] == "" or len(postData["edit_tasks"]) < 1:
            errors.append("All fields must be filled out!")
            print "all fields must fill out pop out"
        if errors == []:
            update_time= self.filter(id = app_id).update(task = postData['edit_tasks'], status = postData['edit_status'], time = postData['edit_time'], date = postData['edit_date'])

            return (True, update_time)
        else:
            return (False, errors)

class Appointment(models.Model):
    user= models.ForeignKey(User, related_name="onrecord", blank=True, null=True)
    task= models.CharField(max_length=255)
    status= models.CharField(max_length=255)
    date= models.DateField(blank=True, null=True)
    time= models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    objects= appointManager()
