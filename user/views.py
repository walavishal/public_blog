from django.shortcuts import render,redirect
from .models import Myblog,usr
from datetime import datetime
import stripe
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt


stripe.api_key=settings.STRIPE_SECRET_KEY

# Create your views here.


def home(request):
    data=Myblog.objects.all().order_by('-date','-time')
    if 'email' in request.session:
        p=usr.objects.get(email=request.session['email'])
        premium=p.premium
    else:
        premium=False
    
    return render(request,'home.html',{'dt':data,'premium':premium})

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
        d=usr.objects.get(email=request.session['email'])
        if (d.blog_view_count<10 and d.join_date<=datetime.now().date()<=d.expiry_date) or d.premium==True:
            d.blog_view_count=d.blog_view_count+1
            d.save()
            data=Myblog.objects.get(id=id)
            return render(request,'fullview.html',{'dt':data})
        else:
            return render(request,'home.html',{'a':1})    
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
    print("Webhook")
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
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
    #NEW CODE
        session = event['data']['object']
        email=session["metadata"]["email"]
    #Updating order
    data=usr.objects.get(email=email)
    data.premium=True
    data.save()
       
    print('helo hoob')
    return HttpResponse(status=200)
