from django.shortcuts import render
import pyrebase
import json


from django.contrib import auth
from django.http import HttpResponse
config = {
    "apiKey": "AIzaSyCE3aBjH1LiOcAZ_GG3d7lgFhXZ3Q8gIb8",
    "authDomain": "inf551-d17d1.firebaseapp.com",
    "databaseURL": "https://inf551-d17d1.firebaseio.com",
    "projectId": "inf551-d17d1",
    "storageBucket": "inf551-d17d1.appspot.com",
    "messagingSenderId": "1051148253779",
    "appId": "1:1051148253779:web:105a4f728be6f062db64a6",
    "measurementId": "G-4B5X2KPSJQ"


  }

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database=firebase.database()
def signIn(request):

    return render(request, "signIn.html")

def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message="invalid credentials"
        return render(request,"signIn.html",{"messg":message})
    print(user['idToken'])
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request, "welcome.html",{"e":email})
def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')
def signUp(request):
    return render(request,"signUp.html")
#create an account:
def postsignup(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    passwd=request.POST.get('pass')
    try:
        user=authe.create_user_with_email_and_password(email,passwd)
    except:
        message="At least 6 charactors for password"
        return render(request,"signUp.html",{"messg":message})
    return render(request,'signIn.html')
def getdata(request):
    dataset='world'
    keyword=request.GET.get('search')
    keyword=keyword.split(' ')

    result = []
    for i in keyword:
        m=i.lower()
        value = database.child(dataset).child('index').child(m).get().val()
        result += value
    # print(len(result))
    #delete the duplicate element in the result
    temp = []
    for item in result:
        if not item in temp:
            temp.append(item)
    # print(len(temp))
    fin_dic = {}
    for item in temp:
        n = result.count(item)
        fin_dic[n] = item
    fin_dic = sorted(fin_dic.items(), key=lambda fin_dic: fin_dic[0], reverse=True)
    ranked_result=[]
    for i in fin_dic:
        ranked_result.append(i[1])

    return render(request,'results.html',{'data_list':json.dumps(ranked_result)})
def selectdata(request):
    pri_key=request.GET['name']
    table=request.GET['table']
    value = database.child(table).child(pri_key).get().val()
    return render(request,'navigate.html',{'data':json.dumps(value)})



