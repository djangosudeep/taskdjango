from django.shortcuts import render, redirect
from google_play_scraper import app
import pyrebase
 
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

def home(request):
    appData = {}
    if request.method == 'POST':
        appname = request.POST['appname']
        applink = request.POST['applink']

        result = app(
            applink,
            lang = 'en'
        )
        appData['appname'] = appname
        appData['applink'] = applink
        appData['category'] = result['genre']
        appData['icon'] = result['icon']
        appData['website'] = result['developerWebsite']


        return render(request, 'adsite/home.html',{'data': appData})

    else:
        return render(request, 'adsite/home.html')

userloggedin = False
def submit(request):

    if(userloggedin):

        

        if request.method == 'POST':
            appName = {}
            appData = {}

            appname = request.POST['appname']
            appData['applink'] = request.POST['applink']
            appData['icon'] = request.POST['icon']
            appData['website'] = request.POST['website']
            appData['points'] = request.POST['points']
            appData['category'] = request.POST['cat']

            appName[appname] = appData

            
            try:
                allAppsData = database.child('apps').get()
                for i in allAppsData.each():
                    for a,b in i.val().items():
                        if a == appname:
                            print("app already exists")
                        else:
                            database.child('apps').push(appName)
                            return render(request, 'adsite/home.html')
            except:
                database.child('apps').push(appName)
                return render(request, 'adsite/home.html')
                

        else:

            try:

                allAppsData = database.child('apps').get()

                return render(request, 'adsite/index.html', {'appsdata':allAppsData})
            except:
                return render(request, 'adsite/index.html')

    else:
        return redirect('/login')








def login(request):

    global userloggedin

    user_data = database.child('users').get()

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        email_list = [];
        password_list = []
        for i in user_data.each():
            for a,b in i.val().items():
                if(a == "email"):
                    email_list.append(b)
                elif(a == "password"):
                    password_list.append(b)

        
        for a in range(len(email_list)):
            for b in range(len(password_list)):
                if(a == b):
                    print(a,b , email, password)
                    if(email_list[a] == email and password_list[b] == password):
                        print("working", userloggedin)
                        userloggedin = True
                        return redirect('/')

                    else:

                        print("not working")
                        return redirect('/login')
    else:
        
        return render(request, 'adsite/login.html')

def register(request):
    user_data = {}
    if request.method == 'POST':
        user_data['username'] = request.POST['username']
        user_data['email'] = request.POST['email']
        user_data['password'] = request.POST['password']

        database.child('users').push(user_data)

        return redirect('/login')
    else:
        return render(request, 'adsite/register.html')