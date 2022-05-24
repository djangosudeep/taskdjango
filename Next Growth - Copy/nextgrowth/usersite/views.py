from django.shortcuts import render, redirect
from google_play_scraper import app
import pyrebase
from django.core.files.storage import default_storage   
import os
from rest_framework import viewsets

config={
    'apiKey': "AIzaSyCWmw5A1pE5WDHoRTHy95dzbY8cGsWCT_w",
    'authDomain': "nextgrowth-648c0.firebaseapp.com",
    'projectId': "nextgrowth-648c0",
    'databaseURL' : 'https://nextgrowth-648c0-default-rtdb.firebaseio.com/',
    'storageBucket': "nextgrowth-648c0.appspot.com",
    'messagingSenderId': "907014894314",
    'appId': "1:907014894314:web:f2603c1ff0051cfe4f9d93",
    'measurementId': "G-3Z5EWXXVBV"
}
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
storage = firebase.storage()



def home(request):
    if('userloggedin' in request.session):

        username = request.session.get('username')

        allAppsData = database.child('apps').get()
    
        return render(request, 'usersite/index.html', {'appsdata': allAppsData, 'username': username})
    else:
        return redirect('http://127.0.0.1:8000/user/login')


def appdetails(request,task):

    appname = task
    username = request.session.get('username')
    allAppsData = database.child('apps').get()

    appinfo = {}

    for i in allAppsData.each():
        for a, b in i.val().items():

            if(a == appname):
                appinfo['icon'] = b['icon']
                appinfo['appname'] = appname
                appinfo['website'] = b['website']
                appinfo['category'] = b['category']
                appinfo['points'] = b['points']


    if request.method == 'POST':
        appId = 0
        tasks = {}
        usertasks = {}
        appn = request.POST['appname']
        tasks['username'] = username
        tasks['app'] = request.POST['appname']
        tasks['points'] = request.POST['points']
        tasks['category'] = request.POST['category']

        usertasks[username] = tasks
        task_completed = True
        try:
            check_task = database.child('user_tasks').child(username).get()
            for i in check_task.each():
                print("values: ", i.val(), i.key())
                if(i.key() != 0):
                    for a,b in i.val().items():
                        print('these are the files: ',a,username)
                        if(a == username):
                            print(b['app'])
                            if(b['app'] == appn):
                                task_completed = False
                                print("app already added")
                            else:
                                print("Done")
                            

            if(task_completed):
                msg = "Task Has Been Successfully Completed"
                try:
                    aid = database.child('user_tasks').child(username).get()
                    for i in aid.each():
                        if(i.key() != 0 and i.key() == 1):
                            print("task appid: ", appId+ i.key() + 1)
                            appId += i.key()
                            appId += 1
                        elif(i.key() > 1):
                            appId += i.key()

                    
                    appId = str(appId)
                   
                    database.child('user_tasks').child(username).child(appId).set(usertasks)
                    return render(request, 'usersite/message.html', {'msg': msg})
                                
                except Exception as e:
                    print("nothing: ",e)
                
            else:
                msg = "Already Completed The Task For this app"
                
                return render(request, 'usersite/message.html', {'msg': msg})


        except Exception as e:
            appId += 1
            appId = str(appId)
            database.child('user_tasks').child(username).child(appId).set(usertasks)
            print("error: " + str(e))

        return render(request, 'usersite/appdetail.html', {'appinfo': appinfo, 'username': username})
    else:
        return render(request, 'usersite/appdetail.html', {'appinfo': appinfo, 'username': username})



def profile(request):
    username = request.session.get('username')
    userdata = database.child('users').get()
    useremail = ""
    for i in userdata.each():
        for a,b in i.val().items(): 
            if(a == "username" and b == username):
                useremail += i.val()['email']
    return render(request, 'usersite/profile.html', {'username': username,'useremail': useremail})



def points(request):

    username = request.session.get('username')
    userdata = database.child('user_tasks').child(username).get()
    userpoints = 0
    try:
        for i in userdata.each():
            if(i.key() != 0):
                for a,b in i.val().items(): 

                    userpoints += int(b['points'])

    except Exception as e:
        print("error: ",e)

    return render(request, 'usersite/points.html', {'points': userpoints, 'username': username})



def tasks(request):
    username = request.session.get('username')
    appdetails = {}
    apppoints = []
    userdata = database.child('user_tasks').child(username).get()
    try:
        for i in userdata.each():
            if(i.key() != 0):
                for a,b in i.val().items():
                    appdetails[b['app']] = b['points']

    except Exception as e:
        print("error: ",e)
   
    return render(request, 'usersite/task.html', {'apppoints': appdetails,'username': username})


def login(request):

    user_data = database.child('users').get()

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        email_list = []
        password_list = []
        username_list = []
        for i in user_data.each():
            for a,b in i.val().items():
                if(a == "email"):
                    email_list.append(b)
                elif(a == "password"):
                    password_list.append(b)
                elif(a == "username"):
                    username_list.append(b)

        
        for a in range(len(email_list)):
            for b in range(len(password_list)):
                if(a == b):
                    print(a,b , email, password)
                    if(email_list[a] == email and password_list[b] == password):
                        print("this is email: ", email_list[a])
                        
                        request.session['userloggedin'] = True

                        request.session['username'] = username_list[a]
                        return redirect('http://127.0.0.1:8000/user/home')

                    else:
                        pass



    else:
        if('userloggedin' in request.session):
            return redirect('http://127.0.0.1:8000/user/home')
        else:
            return render(request, 'usersite/login.html')


def logout(request):
    del request.session['username']
    del request.session['userloggedin']
    return redirect('http://127.0.0.1:8000/user/login')

def register(request):
    user_data = {}
    if request.method == 'POST':
        user_data['username'] = request.POST['username']
        user_data['email'] = request.POST['email']
        user_data['password'] = request.POST['password']

        database.child('users').push(user_data)

        return redirect('http://127.0.0.1:8000/user/login')
    else:
        return render(request, 'usersite/register.html')




#Exposing the api data


def apifetch(request):

    username = request.session.get('username')

    return render(request, 'usersite/api.html', {'username': username})