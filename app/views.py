from django.shortcuts import render
from django.http import HttpResponse
from app.models import *
from app.forms import *
from django.core.mail import send_mail

# Create your views here.

def Registration(request):
    udata=Userform() ## collect userform data
    pdata=Profileform()  ## collect Profile form data
    d={'udata':udata,'pdata':pdata} # to display the forms in FE
    if request.method=='POST' and request.FILES: 
        usfd=Userform(request.POST)   ## In useform v r having only data so v use only request.POST
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
                      'whateveritmaybe000@gmail.com',[nsusfd.email],fail_silently=True)

            return HttpResponse('Data Submitted succefully')

    return render(request,'Registration.html',d)