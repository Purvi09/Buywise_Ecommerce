from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .models import Contact, Product, Orders, OrderUpdate
from math import ceil
import razorpay
from django.contrib.sites.shortcuts import get_current_site
from .keys import razorpay_id,razorpay_account_id
from django.views.decorators.csrf import csrf_exempt

def index(request):
    allProds = []
    catprods = Product.objects.values('category','id')
    print(catprods)
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params= {'allProds':allProds}
    return render(request,'index.html',params)

def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        desc=request.POST.get("desc")
        pnumber=request.POST.get("pnumber")
        myquery=Contact(name=name,email=email,desc=desc,phonenumber=pnumber)
        myquery.save()
        messages.info(request,"we will get back to you soon..")
        return render(request,"contact.html")
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

razorpay_client = razorpay.Client(auth=(razorpay_id, razorpay_account_id))
def checkout(request):
    print("Hi")
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')

    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = int(request.POST.get('amt'))
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        Order = Orders(items_json=items_json,name=name,amount=amount, email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
        print(amount)
        Order.save()
        update = OrderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
        update.save()
        thank = True
        order_currency = 'INR'
        
        callback_url = 'http://127.0.0.1:8000/handlerequest/'
        notes = {'order-type': "basic order from the website", 'key':'value'}
        razorpay_order = razorpay_client.order.create(dict(amount=amount*100, currency=order_currency, notes = notes, receipt=str(Order.order_id), payment_capture='0'))
        print(razorpay_order['id'])
        Order.razorpay_order_id = razorpay_order['id']
        Order.save()
        
        return render(request, 'razorpay.html', {'order':Order, 'orderId':Order.order_id, 'order_id': razorpay_order['id'],'final_price':amount, 'razorpay_merchant_id':razorpay_id, 'callback_url':callback_url})
    

    return render(request,'checkout.html')
@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            print(payment_id)
            order_id = request.POST.get('razorpay_order_id','')
            print(order_id)
            signature = request.POST.get('razorpay_signature','')
            print(signature)
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            try:
                order_db = Orders.objects.get(razorpay_order_id=order_id)
                order_db.amountpaid=order_db.amount
                order_db.razorpay_payment_id = payment_id
                order_db.razorpay_signature = signature
                order_db.save()
                result = razorpay_client.utility.verify_payment_signature(params_dict)
                print(result)
                if result==True:
                    order_db.paymentstatus="success"
                    return render(request,'paymentsuccess.html')
                else:
                    order_db.paymentstatus="fail"
                    return render(request,'paymentfail.html')
            except:
                return HttpResponse("505 Not Found")
            
        except Exception as e:
            print(e)
            return HttpResponse("505 not found")
        
def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')
    currentuser=request.user.username
    items=Orders.objects.filter(email=currentuser)
    rid=0
    for i in items:
        print(i.order_id)
        myid=i.order_id
        rid=myid
        print(rid)
    status=OrderUpdate.objects.filter(order_id=rid)
    # for j in status:
    #     print(j.update_desc)

   
    context ={"items":items,"status":status}
    # print(currentuser)
    return render(request,"profile.html",context)


