from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from app.models import *
from app.forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def Registration(request):
    udata=Userform() ## collect userform data
    pdata=Profileform()  ## collect Profile form data
    d={'udata':udata,'pdata':pdata} # to display the forms in FE
    if request.method=='POST' and request.FILES: 
        usfd=Userform(request.POST)   ## In userform v r having only data so v use only request.POST
        pfd=Profileform(request.POST,request.FILES) # In Profile form v r having both data&images/files so v use both request.POST, request.FILES
        if usfd.is_valid() and pfd.is_valid():  # checking both data valid or not
            nsusfd=usfd.save(commit=False)  # it collects data but not save now
            password=usfd.cleaned_data['password']
            nsusfd.set_password(password)
            nsusfd.save()

            nspfd=pfd.save(commit=False)
            nspfd.username=nsusfd
            nspfd.save()

            send_mail('Registration',
                      'Congratulations! You have successfully registered on the Django application',
                      'whateveritmaybe000@gmail.com',
                      [nsusfd.email],
                      fail_silently=True)

            return HttpResponse('Data Submitted succefully')

    return render(request,'Registration.html',d)


def home(request):
     if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
     
     return render(request,'home.html')

def userlogin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('Not a Active User')
        else:
            return HttpResponse('Invalid Details')
        
    return render(request,'userlogin.html')


@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_details(request):
    username=request.session.get('username')  ## getting details from the sesssion 
    uo=User.objects.get(username=username)   ## get details of username using quesry set
    po=Profile.objects.get(username=uo)  
    d={'uo':uo,'po':po}
    return render(request,'display_details.html',d)

@login_required
def changepassword(request):
    if request.method=='POST':
        password=request.POST['password']
        username=request.session.get('username')
        uo=User.objects.get(username=username)
        uo.set_password(password)
        uo.save()
        return HttpResponse('password change succesfully')
    return render(request,'changepassword.html')

def reset_password(request):
    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']
        luo=User.objects.filter(username=un)
        if luo:
            uo=luo[0]
            uo.set_password(pw)
            uo.save()
            return HttpResponse('Reset password is Done')
        else:
            return HttpResponse('Invalid user details')
    return render(request,'reset_password.html')