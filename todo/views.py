from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout,authenticate
from .forms import TodoForm
from .models import Todo
from .models import AboutUser
from .models import Comment
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File  
import urllib






# Create your views here.

def home(request) :
    return render(request,'index.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request,'todo/loginuser.html')
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'todo/signupuser.html',{'error':'username and password does not match'})
        else:
            if user.first_name == '':
                login(request,user)
                return redirect('privatepage')
            else:
                try:
                    vcode = get_random_string(length=6, allowed_chars='1234567890')
                    subject = 'EMAIL VERIFICATION'
                    message = 'Your verification code is :' + vcode
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [request.POST['email'],]
                    send_mail( subject, message, email_from, recipient_list )
                    user.first_name = vcode
                    user.save()
                    return render(request,'todo/emailsign.html',{'email':request.POST['email'],'username':request.POST['username']})

                except IntegrityError:
                    return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'The username has already been taken, please choose another username'})

                
                

def signupuser(request):
    if request.user.is_authenticated:
        return redirect('privatepage')
    else:
        if request.method == 'GET':
            return render(request,'todo/signupuser.html',{'form':UserCreationForm()})
        else:
            #create a new user
            if request.POST['password1'] == request.POST['password2']:
                try:
                    vcode = get_random_string(length=6, allowed_chars='1234567890')
                    subject = 'EMAIL VERIFICATION'
                    message = 'Your verification code is :' + vcode
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [request.POST['email'],]
                    send_mail( subject, message, email_from, recipient_list )
                    user = User.objects.create_user(request.POST['username'],password = request.POST['password1'],email=request.POST['email'],first_name=vcode)
                    aboutuser = AboutUser(user=user)
                    aboutuser.save()
                    user.save()
                    return render(request,'todo/emailsign.html',{'email':request.POST['email'],'username':request.POST['username']})

                except IntegrityError:
                    return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'The username has already been taken, please choose another username'})

            else:
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'passwords did not match'})


@login_required
def privatepage(request):
    todos = Todo.objects.filter(user=request.user).order_by('-created')
    return render(request,'newprivate.html',{'todos':todos})

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request,'todo/createtodo.html',{'form':TodoForm()})
    else:
        try:
            # form = TodoForm(request.POST,request.FILES)

            # if form.is_valid(): 
            #     ftitle = form.cleaned_data.get("title")
            #     # fimg = request.FILES['pic']
            #     fmemo = form.cleaned_data.get('memo')
            #     fprivate = form.cleaned_data.get('private')
            #     obj = Todo.objects.create(
            #         title = ftitle,
            #         memo = fmemo,
            #         private = fprivate,
            #         user = request.user
            #     )
            #     if request.FILES.get('pic',False) :
            #         obj.pic = request.FILES['pic']
                    
            #     obj.save()

            post = Todo.objects.create(
                title = request.POST['title'],
                memo = request.POST['content'],
                user = request.user
            )
            if request.POST['private'] == "1":
                post.private = True
            else:
                post.private = False

            if request.FILES.get('pic',False) :
                post.pic = request.FILES['pic']
            
            post.save()

            return redirect('privatepage')  
        except ValueError:
            return render(request,'todo/createtodo.html',{'form':TodoForm(),'error':'Bad data passed in. try again'})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request,'todo/viewtodo.html',{'todo':todo,'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos') 
        except ValueError:
            return render(request,'todo/viewtodo.html',{'form':form, 'todo':todo ,'error':'Bad data passed in. try again'})

@login_required
def completetodo(request,todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request,todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user).order_by('-created')
    return render(request,'todo/completedtodos.html',{'todos':todos})

def verify(request):
    code = request.POST['1'] + '' + request.POST['2'] + '' + request.POST['3'] + '' + request.POST['4'] + '' + request.POST['5'] + '' + request.POST['6']
    user = get_object_or_404(User,username=request.POST['username'])
    ucode = user.first_name
    error = 'the code you entered was wrong, please try again.'
    if code != ucode:
        return render('todo/emailsign.html',{'email':request.POST['email'],'username':request.POST['username'],'error':error})
    else:
        login(request,user)
        user.first_name = ''
        user.save()
        return redirect('privatepage')



def faq(request):
    return render(request,'faq.html')

def contactus(request):
    if request.method == 'GET':
        return render(request,'contactus.html')
    else:
        useremail = request.POST['email']
        usermessage = request.POST['message']
        subject = '!!!!!!!!!!!!!!!!--USER QUESTION--!!!!!!!!!!!!!!!!'
        message = 'Hello admin, username: @' + request.user.username + '\nwith email address of : ' + useremail +  '\nasked the following question:                \n\n' + usermessage
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['kavand.hossain@gmail.com']
        send_mail( subject, message, email_from, recipient_list )
        return render(request,'tyemail.html')

@login_required
def profile(request):
    user = request.user
    aboutuser = get_object_or_404(AboutUser,user=request.user)
    posts = todos = Todo.objects.filter(user=request.user).order_by('-created')
    return render(request,'profile.html',{'user':user,'aboutuser':aboutuser,'posts':posts})

@login_required
def editprofile(request):
    user = request.user
    aboutuser = get_object_or_404(AboutUser,user=request.user)
    if request.method == 'GET':
        return render(request,'editprofile.html',{'user':user,'aboutuser':aboutuser})
    else:
        user.last_name = request.POST['fullname']
        aboutuser.slogan = request.POST['slogan']
        aboutuser.bio = request.POST['bio']
        if request.FILES.get('pic',False) :
            aboutuser.pic = request.FILES['pic']

        user.save()
        aboutuser.save()
        return redirect('profile')

def fullstory(request):
    post = get_object_or_404(Todo,pk=request.POST['post_pk'])
    comments = Comment.objects.filter(postid=request.POST['post_pk']).order_by('-date')
    aboutauthor = get_object_or_404(AboutUser,user=post.user)
    for comment in comments:
        img = get_object_or_404(AboutUser,user=comment.authoruser)
        comment.pic = img.pic
    return render(request,'fullstory.html',{'post':post,'comments':comments,'about':aboutauthor})

@login_required
def savecomment(request):
    comment = Comment.objects.create(
        authoruser = request.user,
        postid = request.POST['post_pk'],
        text = request.POST['message']
    )
    comment.save()
    post = get_object_or_404(Todo,pk=request.POST['post_pk'])
    comments = Comment.objects.filter(postid=request.POST['post_pk']).order_by('-date')
    aboutauthor = get_object_or_404(AboutUser,user=post.user)
    for comment in comments:
        img = get_object_or_404(AboutUser,user=comment.authoruser)
        comment.pic = img.pic
    return render(request,'fullstory.html',{'post':post,'comments':comments,'about':aboutauthor})

def viewprofile(request,user_username):
    person = get_object_or_404(User,username=user_username)
    aboutperson = get_object_or_404(AboutUser,user=person)
    posts = Todo.objects.filter(user=person).order_by('-created')
    return render(request,'person.html',{'person':person,'about':aboutperson,'posts':posts})

@login_required
def editstory(request,post_pk):

    if request.method == 'GET':
        post = get_object_or_404(Todo,pk=post_pk)
        if request.user == post.user:
            return render(request,'editstory.html',{'post':post})
        else:
            return render(request,'error.html',{'error':'This story does not belong to you, so you dont have permission to edit it.'})  
    else:
        # post_pk = request.POST['post_pk']
        post = get_object_or_404(Todo,pk=post_pk)
        if request.user == post.user:
            post.title = request.POST['title']
            post.memo = request.POST['content']
            print(request.FILES)
            if request.FILES.get('pic',False) :
                post.pic = request.FILES['pic']
            if request.POST['private'] == "1":
                post.private = True
            else:
                post.private = False
            post.save()
            return redirect('privatepage')
        else:
            return render(request,'error.html',{'error':'This story does not belong to you, so you dont have permission to edit it.'})
@login_required
def deletestory(request):
    if request.method == 'POST':
        try:
            post = get_object_or_404(Todo,pk=request.POST['post_pk'],user=request.user)
            post.delete()
            return redirect('privatepage')
        except:
            return render(request,'error.html',{'error':'this post does not beong to you, so you cant delete it.'})



def globalspace(request):
    posts = Todo.objects.filter(private=False).order_by('-created')
    return render(request,'global.html',{'posts':posts})