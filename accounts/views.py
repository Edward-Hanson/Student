from django.contrib.auth import login, authenticate
from django.shortcuts import render,redirect
from django.contrib import messages


from .forms import LoginForm




# Create your views here.
def student_login(request):
    if request.user.is_authenticated:
       return redirect('home')
    
    if request.method=="POST":
        form= LoginForm(request.POST)
        if form.is_valid():
            student_id= form.cleaned_data['student_id']
            password = form.cleaned_data['password']
            user = authenticate(request,student_id= student_id, password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return redirect('home')
                messages.info(request,"Please activate your account")
            messages.info(request,"Wrong Email or Password")
            return redirect('login')
    else:
        form = LoginForm()
    return render(request,'registration/login.html',{'form':form})  
        