from django.shortcuts import render,redirect
from .models import Myblog,usr,image
from datetime import datetime,timedelta
import stripe
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import os

load_dotenv()


stripe.api_key=os.getenv('STRIPE_SECRET_KEY')

# Create your views here.


def home(request):
    data=Myblog.objects.all().order_by('-date','-time')
    
    if 'email' in request.session:
        p=usr.objects.get(email=request.session['email'])
        premium=p.premium
    else:
        premium=False
    response = HttpResponse(render(request,'home.html',{'dt':data,'premium':premium}))  
    if 'count' in request.COOKIES:
        pass
    else:
        response.set_cookie('count',0)  
        response.set_cookie('c_date',datetime.now().date())
    
    return response

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
        imag=request.FILES['image']

        x=datetime.now()

        
        x=str(x.year)+str(x.month)+str(x.day)+str(x.hour)+str(x.minute)+str(x.second)
        blog=Myblog(blog_id=x,topic=topic,content=content,email=email,name=name)
        
        if blog.save():
            return redirect("/createblog")
        else:
            imag.name=x+imag.name
            blog=Myblog.objects.get(blog_id=x)
            img=image(blog_id=blog,image_path=imag)
            img.save()
            return redirect("/")
            
        

def viewfullblog(request,id):
    count=int(request.COOKIES['count'])
    c_date=datetime.strptime(request.COOKIES['c_date'], "%Y-%m-%d").date()
    

   
    if 'email' in request.session:
        d=usr.objects.get(email=request.session['email'])
        if (d.blog_view_count<10 and d.join_date<=datetime.now().date()<=d.expiry_date) or d.premium==True:
            d.blog_view_count=d.blog_view_count+1
            d.save()
            data=Myblog.objects.get(blog_id=id)
            a=image.objects.get(blog_id=id)
            data.image_path=a.image_path#this will not prmanent add image_path to myblog
            return render(request,'fullview.html',{'dt':data})
        else:
            return render(request,'home.html',{'a':1})    
    else:
        if count<=10 and (c_date<=datetime.now().date()<=(c_date+timedelta(days=30))):
            data=Myblog.objects.get(blog_id=id)
            a=image.objects.get(blog_id=id)
            data.image_path=a.image_path#this will not prmanent add image_path to myblog
            response = HttpResponse(render(request,'fullview.html',{'dt':data}))
            response.set_cookie('count',count+1)
            return response
        else:
             return render(request,'home.html',{'b':1}) 
        
   

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
    ct=Myblog.objects.filter(email=request.session['email'],blog_id=id).count()
    if 'email' in request.session and ct==1:
        data=Myblog.objects.filter(blog_id=id,email=request.session['email'])
        return render(request,'edit.html',{'dt':data[0]})#above return list of object so we only need 1
    else:
        return redirect('/login')
    
def editvalidate(request):
    id=request.POST.get('id')
    topic=request.POST.get('topic')
    content=request.POST.get('content')
    imag=request.FILES['image']
    ct=Myblog.objects.filter(email=request.session['email'],blog_id=id).count()
     
    if ct ==1:
        data=Myblog.objects.get(email=request.session['email'],blog_id=id)
        data.topic=topic
        data.content=content
        data.save()
        b=image.objects.get(blog_id=data)
        b.delete()
        x=datetime.now()
        x=str(x.year)+str(x.month)+str(x.day)+str(x.hour)+str(x.minute)+str(x.second)
        imag.name=x+imag.name
        img=image(blog_id=data,image_path=imag)
        img.save()
        return redirect('/myblogs')
    else:
        return render(request,'edit.html',{'err':1})
def delete(request,id):
    ct=Myblog.objects.filter(email=request.session['email'],blog_id=id).count()
     
    if ct ==1:
        data=Myblog.objects.get(email=request.session['email'],blog_id=id)
        b=image.objects.get(blog_id=data)
        b.delete()# first image object will be deleted and than blog  to delete image from physical location we have override delete method o image object
        data.delete()
        return redirect('/myblogs')
    else:
        return redirect('/myblogs')
def viewpersonal(request,id):
    if 'email' in request.session:
        data=Myblog.objects.get(blog_id=id)
        img=image.objects.get(blog_id=data)
        data.image=img.image_path
        return render(request,'viewfull_personal.html',{'dt':data})
    else:
        return render(request,'login.html')
    

def checkout(request):
    return render(request,'checkout.html')




#****************below code for payment***************

@csrf_exempt
def create_checkout_session(request):
    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
    'price_data': {
    'currency': 'inr',
    'product_data': {
    'name': 'Premium Blog',
    },
    'unit_amount': 39900,
    },
    'quantity': 1,
    }],
    metadata={
        'email':request.session['email']
    },
    mode='payment',
    success_url='http://127.0.0.1:8000/success',
    cancel_url='http://127.0.0.1:8000/cancel',
    )
    # print(session)
   
    return JsonResponse({'id': session.id})

def success(request):
    if 'email' in request.session:
        return render(request,'success.html')
    else:
        return redirect('/login')
    

def fail(request):
    if 'email' in request.session:
        return render(request,'fail.html')
    else:
        return redirect('/login')
    

def premium(request):
    if 'email' in request.session:
        return render(request,'premium.html')
    else:
        return redirect('/login')
    

@csrf_exempt
def webhook(request):
   
    endpoint_secret = os.getenv('STRIPE_ENDPOINT_SECRET')
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
    )
    except ValueError as e:
    # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
    # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
   
        session = event['data']['object']
        email=session["metadata"]["email"]
    
    if session['payment_status']=='paid':
        data=usr.objects.get(email=email)
        data.premium=True
        data.save()
    
       
   
    return HttpResponse(status=200)
