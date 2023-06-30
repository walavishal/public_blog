from django.shortcuts import render,redirect
from .models import Myblog,usr,hshddfsdh

# Create your views here.


def home(request):
    data=Myblog.objects.all().order_by('-date','-time')
    return render(request,'home.html',{'dt':data})

def createblog(request):
    if 'email' in request.session:
        return render(request,'createblog.html')
    else:
        return render(request,'login.html')

def saveblog(request):
    if request.method=="POST":
        topic=request.POST.get('topic')
        content=request.POST.get('content')
        email=request.session['email']
        name=request.session['name']
        blog=Myblog(topic=topic,content=content,email=email,name=name)
        if blog.save():
            return redirect("/createblog")
        else:
            return redirect("/")
        

def viewfullblog(request,id):
    if 'email' in request.session:
        data=Myblog.objects.get(id=id)
        return render(request,'fullview.html',{'dt':data})
    else:
        return render(request,'login.html')
   

def login(request):
    return render(request,'login.html')
def register(request):
    return render(request,'register.html')

def registeruser(request):
    name=request.POST.get('name')
    emai=request.POST.get('email')
    password=request.POST.get('password')
    count=usr.objects.filter(email=emai).count()
    if count==0:
        data=usr(name=name,email=emai,password=password)
        data.save()
        return redirect('/login')
    else:
        return render(request,'register.html',{'dt':1})

def loginvalidate(request):
        email=request.POST.get('email')
        pwd=request.POST.get('password')
        data=usr.objects.filter(email=email,password=pwd).count()
        data1=usr.objects.filter(email=email,password=pwd)#return objects whosse value is provided in filter
        if data==1:
            if 'name' in request.session and 'email' in request.session:
                del request.session['name']
                del request.session['email']
            request.session['name']=data1[0].name
            request.session['email']=data1[0].email
            return redirect('/')
        else:
             return render(request,'login.html',{'dt':1})            

def logout(request):
    del request.session['name']
    del request.session['email']
    return redirect('/')

def myblogs(request):
    if 'email' in request.session:
        data=Myblog.objects.filter(email=request.session['email']).order_by('-date','-time')
        return render(request,'myblogs.html',{'dt':data})
    else:
        return redirect('/login')
    
def edit(request,id):
    ct=Myblog.objects.filter(email=request.session['email'],id=id).count()
    if 'email' in request.session and ct==1:
        data=Myblog.objects.filter(id=id,email=request.session['email'])
        return render(request,'edit.html',{'dt':data[0]})#above return list of object so we only need 1
    else:
        return redirect('/login')
    
def editvalidate(request):
    id=request.POST.get('id')
    topic=request.POST.get('topic')
    content=request.POST.get('content')
    ct=Myblog.objects.filter(email=request.session['email'],id=id).count()
     
    if ct ==1:
        data=Myblog.objects.get(email=request.session['email'],id=id)
        data.topic=topic
        data.content=content
        data.save()
        return redirect('/myblogs')
    else:
        return render(request,'edit.html',{'err':1})
def delete(request,id):
    ct=Myblog.objects.filter(email=request.session['email'],id=id).count()
     
    if ct ==1:
        data=Myblog.objects.get(email=request.session['email'],id=id)
        data.delete()
        return redirect('/myblogs')
    else:
        return redirect('/myblogs')
def viewpersonal(request,id):
    if 'email' in request.session:
        data=Myblog.objects.get(id=id)
        return render(request,'viewfull_personal.html',{'dt':data})
    else:
        return render(request,'login.html')