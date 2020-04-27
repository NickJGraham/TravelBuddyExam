from django.shortcuts import render, redirect
import bcrypt
from .models import *
from django.contrib import messages
from django.db.models import Q


def index(request):
    return render(request, 'index.html')

#Registering a New User

def register_User(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hash1 = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
        new_User = User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hash1)
        request.session['userid'] = new_User.id
        return redirect('/home')

#Home Page Display

def Home(request):
    user = User.objects.get(id = request.session['userid'])
    context = {
        "User_html": user,
        "trips": Trip.objects.filter(Q(createdBy = user) | Q(tripMembers = user)),
        "otherTrips": Trip.objects.exclude(Q(createdBy = user) | Q(tripMembers = user)),
    }
    return render(request, 'home.html', context)

#Login 

def login(request):
    try:
        User.objects.get(username = request.POST['username'])
    except:
        messages.error(request, 'This User does not exist.')
        return redirect('/')
    user = User.objects.get(username = request.POST['username'])
    request.session['loggedinId'] = user.id
    if bcrypt.checkpw(request.POST["password"].encode(), user.password.encode()):
        request.session['userid'] = user.id
        return redirect('/home')
    else:
        messages.error(request, "Incorrect password.")
        return redirect('/')


#Log Out

def logout(request):
    request.session.clear()
    return redirect('/')

#Add a trip route

def addTrip(request):
    return render(request, 'add_trip.html')

#Add and process Trip to database

def processTrip(request):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/addTrip")
    user = User.objects.get(id = request.session['userid'])
    newTrip = Trip.objects.create(destination = request.POST['destination'], startDate = request.POST['dateFrom'], endDate = request.POST['dateTo'], plan = request.POST['description'], createdBy = user)
    return redirect('/home')

#Destination Page
def showDestination(request, destinationId):
    context = {
        'destinationToShow': Trip.objects.get(id = destinationId),
        'planner': User.objects.get(id = (Trip.objects.get(id=destinationId).createdBy_id)),
        'otherUsers': User.objects.filter(joinedTrips = destinationId).exclude(id = (Trip.objects.get(id = destinationId).createdBy_id))
    }
    return render(request, "destination.html", context)

#Join Trip
def joinTrip(request, destinationId):
    user = User.objects.get(id = request.session['userid'])
    trip = Trip.objects.get(id = destinationId)
    trip.tripMembers.add(user)
    return redirect('/home')
