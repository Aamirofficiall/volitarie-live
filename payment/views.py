from django.shortcuts import render,redirect,reverse
from django.contrib.auth.decorators import login_required
from .models import *
import stripe
stripe.api_key = "sk_test_xtFEYACuznoTkOyg4R7JvBjy002OVcQvjp"

def getPayment(data):
    if data == 'on':
        return 9900
    elif data == 'package2':
        return 19900
    elif data == 'package3':
        return  49900    

def getOrderOption(data):
    if data == 'on':
        return 'Starter'
    elif data == 'package2':
        return 'Pro'
    elif data == 'package3':
        return  'Enterprise'    


@login_required(login_url='login')
def package(request):
    if request.method=='POST':
        print('###################################')
        print(request.POST['package'])
        print('###################################')

        return redirect('payment',args=request.POST['package'])
    return render(request,'package.html')



@login_required(login_url='login')
def payment(request,args):
    if request.method == 'POST':
        print(request.POST['stripeToken'])
        amount=getPayment(args)
        order_option=getOrderOption(args)
        order=Order.objects.update_or_create(user=request.user,defaults={"order_option": order_option})

        customer=stripe.Customer.create(
            email=request.user.email,
            source=request.POST['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer,
            amount=amount,
            currency='usd',
            description ='Donation'
        )
        if charge['status'] == 'succeeded': 
            payment=Payment.objects.create(
                user=request.user,order=request.user.order,recipt_url=charge['receipt_url'],payment_info=charge)
            print(Balance.objects.filter(user=request.user).count())
            if Balance.objects.filter(user=request.user).count() != 1:
                Balance.objects.create(
                    user=request.user,amount=charge['amount_captured'],remaining_balance=charge['amount_captured'],is_valid=True)
            else:
                Balance.objects.filter(
                    user=request.user).update(
                    amount=Balance.objects.get(user=request.user).remaining_balance+charge['amount_captured'],
                    remaining_balance=Balance.objects.get(user=request.user).remaining_balance+charge['amount_captured'],
                    is_valid=True,
                    )

            return render(request,'success.html',{'recipt':charge['receipt_url']})
        else:
            pass
    
    return render(request,'payment.html')


    


@login_required(login_url='login')
def success(request):

    return render(request,'success.html')
