from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login as dj_login,logout
from app.forms import TODOForm
from django.contrib.auth.forms import AuthenticationForm
from app.models import TODO
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('main')
    return render(request,'index.html')

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else :
        loginusername = request.POST.get('loginuser')
        loginpassword = request.POST.get('loginpassword')

        user= authenticate(username=loginusername,password=loginpassword)
        if user is not None:
            dj_login(request,user)
            return redirect('main')
        else:
            return HttpResponse('Your Credentials are wrong,please try again!')
def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html')
    else :
        name = request.POST.get('user')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        print(name,email,pass1,pass2)
        if pass1 == pass2:
            myuser = User.objects.create_user(username=name,email=email,password=pass1)
            myuser.save()
            return redirect('main')
        else:
            return HttpResponse("Password does't matches")

@login_required(login_url='login')
def main(request):
    if request.user.is_authenticated:
        user = request.user
        todos = TODO.objects.filter(user=user)
        form = TODOForm()
        return render(request,'main.html',context={'form':form,'todos':todos})

def userlogout(request):
    logout(request)
    
    return redirect('home')
        
def addtodo(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            messages.success(request,'todo added')
            return redirect('main')
        else:
            messages.warning(request,'Some error occured')
            return redirect('main')

def deleteTodo(request,id):
    del_toddo = TODO.objects.get(id=id)
    del_toddo.delete()
    return redirect('main')

def updateTodo(request,id):
    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status')
        update_todo = TODO.objects.get(id=id)
        update_todo.title = title
        update_todo.status = status
        update_todo.save()
        return redirect('main')

    else:
        update_todo = TODO.objects.get(id=id)
        return render(request,'update.html',context={'ut':update_todo})