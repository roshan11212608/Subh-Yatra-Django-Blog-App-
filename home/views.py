from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import *;
User = get_user_model()
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
def indexpage(request):
    if(request.user.is_anonymous):
         return redirect("/login")
    
    blogs=Blog.objects.filter(username=request.user)
    
    userData={
                 "firstname":request.user.first_name,
                 "lastname":request.user.last_name,
                 "username":request.user,
                 "profile":f"media/profiles/{request.user.picturename}",
                 "blogs":blogs,

        }   
    return render(request,"index.html",userData)
def loginUser(request):
    if(request.method=="POST"):
         username=str(request.POST.get('email')).split("@")[0]
         password=request.POST.get("password")
         user=authenticate(username=username,password=password)
         confirm=request.POST.get('confirm')
         if(confirm is None):
                messages.warning(request, "⚠️ Please Confirm before Login ! ")
         elif(user is not None):
            login(request,user)
            return redirect('/')
         
         else:
              messages.warning(request,"Please Enter a Valid Credentials !")
              return render(request,'loginUser.html',{})
         

    return render(request,"loginUser.html",{})

def logoutUser(request):
     logout(request)
     return redirect('/login')
def registerUser(request):
    firstname=request.POST.get("firstname")
    lastname=request.POST.get("lastname")
    email=request.POST.get("email")
    password=request.POST.get("password")
    if(request.method=="POST"):
        try:
          file=request.FILES['file']
        except:
             messages.warning(request, "⚠️ Please Select Profile Picture before Register. ⚠️")
             return redirect('/register')
        if(request.POST.get("name")==""):
             messages.warning(request, "⚠️ Please Enter a Valid Name ! ")
        elif(request.POST.get("confirm") is None):
                 messages.warning(request, "⚠️ Please Confirm before Register New User ! ")
        elif(request.POST.get('password')=='' or len(request.POST.get('password'))<10):
              messages.warning(request, "⚠️ Password Can't be Empty or Less than 10 characters ⚠️")
        else:
               try:
                    user=User.objects.create_user(str(email).split('@')[0],email,password)
               except:
                    messages.warning(request, "User Already Exits ! ⚠️ ")
                    return redirect('/login')
               user.first_name=firstname
               user.last_name=lastname
               user.picturename=str(file)
               user.picture=file
               user.save()
               messages.warning(request, "New User Added Successfully ! ")
               return redirect('/login')
    return render(request,"RegisterUser.html",{})

def add(request):
     if(request.user.is_anonymous):
         return redirect("/login")
     userData={
                 "firstname":request.user.first_name,
                 "lastname":request.user.last_name,
                 "username":request.user,
                 "profile":f"media/profiles/{request.user.picturename}",

        } 
     if(request.method=="POST"):
          username=request.user
          title=request.POST.get('title')
          content=request.POST.get('content')
          if(title=='' or len(title)<10):
               messages.warning(request,"Enter a Valid Title ⚠️")
               return redirect('/add')
          elif(content=='' or len(content)<10):
               messages.warning(request,"Enter a Valid Content ⚠️")
               return redirect('/add')
          try:
               vlogImage=request.FILES['vlogImage']
          except:
                 messages.warning(request,"Please Add Image First ⚠️")
                 return redirect('/add')



          vlog=Blog(username=username,title=title,content=content,picture=vlogImage,vlogpicturename=f"media/vlogsimage/{vlogImage}")
          vlog.save()
          messages.success(request,"Added Succesfully.")
          return redirect('/')
     
     return render(request,'add.html',userData)
import os
def delete(request,blog_id):
   
     blogs=Blog.objects.filter(username=request.user)
     delete=blogs[blog_id-1]
     os.remove(delete.vlogpicturename)
     delete.delete()
     messages.success(request,"Blog Deleted Succesfully.")
     return redirect('/')

def update(request,blog_id):
     if(request.user.is_anonymous):
         return redirect("/login")
   
     blogs=Blog.objects.filter(username=request.user)
     oldData=blogs[blog_id-1]
     data={
          "id":blog_id,
          "title":oldData.title,
          "content":oldData.content,
           
     }
     if(request.method=="POST"):
          title=request.POST.get('title')
          content=request.POST.get('content')
          # vlogImage=request.FILES['vlogImage']
          if(title=='' or len(title)<10):
               messages.warning(request,"Enter a Valid Title ⚠️")
               return redirect(f"/update/{blog_id}")
          elif(content=='' or len(content)<10):
               messages.warning(request,"Enter a Valid Content !! ⚠️")
               return redirect(f"/update/{blog_id}")
          try:
               vlogImage=request.FILES['vlogImage']
          except:
                 messages.warning(request,"Please Add Image First !! ⚠️")
                 return redirect(f"/update/{blog_id}")


          blogs=Blog.objects.filter(username=request.user)
        
          update=blogs[blog_id-1]
          os.remove(update.vlogpicturename)
          update.delete()
          blog=Blog(username=request.user,title=title,content=content,picture=vlogImage,vlogpicturename=f"media/vlogsimage/{vlogImage}")
          blog.save()
          messages.success(request,"Blog Updated Succesfully.")
          return redirect('/')
     return render(request,'update.html',data)

def updateprofile(request):
     if(request.method=="POST"):
          try:
              file=request.FILES['newfile']
          except:
               messages.warning(request,"Profile Picture can't be Updated , Please Select Profile Picture first before update !!!")
               return redirect('/')
          u = User.objects.get(username=request.user)
          oldprofile=f"media/profiles/{str(u.picturename)}"
          if(os.path.exists(oldprofile)):
               os.remove(oldprofile)
          u.picture=file
          u.picturename=file
          u.save()
          messages.success(request,"Profile Updated Succesfully.")

     return redirect('/')

def forgotpassword(request):
     if(request.method=="POST"):
          newpassword=request.POST.get('newpassword')
          if(newpassword=='' or len(newpassword)<10):
               messages.warning(request,"Password can't be Updated , Please Enter a valid Password for Update !!!")
               return redirect('/forgotpassword')
          u=User.objects.get(username=request.user)
          u.set_password(newpassword)
          u.save()
          messages.success(request,"Password Updated Succesfully.")
     return redirect('/')
def contact(request):
     if(request.method=="POST"):
          name=request.POST.get('name')
          email=request.POST.get('email')
          message=request.POST.get("message")
          data=Contact(name=name,email=email,message=message)
          data.save()
          messages.success(request,"Data Submitted Successfully.")


     return render(request,'contact.html',{})