import pyrebase
from google_play_scraper import app
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

def aptask():
    

    appDetails = database.child('apps').get()

    for i in appDetails.each():
        for a,b in i.val().items():
            appLink = b['applink']
            appKey = i.key()
            result = app(appLink,lang = 'en')
            appGenre = result['genre']

            database.child('apps').child(appKey).child(a).update({'category': appGenre})

            print("data updated successfully")