from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .hiring_scrapper import Client
from payment.models import * 
import csv
import io

def getMinusAmountInCents(string):
    if string == 'Starter':
        return 0.198 *100
    elif string == 'Pro':
        return 0.165*100
    elif string == 'Enterprise':
        return  0.142  *100

@login_required(login_url='login')
def index(request):
    return render(request, 'hiring.html')

@login_required(login_url='login')
def getHiringData(request):

    if request.method == 'POST' and request.FILES['file']:
        if request.user.balance.is_valid == True:
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                response = HttpResponse(content_type='text/json')
                response['notCSV'] = True

                return response
            
            data_set = csv_file.read().decode('UTF-8')

            io_string = io.StringIO(data_set)
            keyword = []
            location = ''
            maxPages = ''

            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                keyword.append(column[0])
                location = column[1]
                maxPages = column[2]

            client = Client()
    
            keyword.pop(0)
            try:
                results = client.search(keywords=keyword, location="New York", maxPages=int(maxPages))
            except:
                results={}


            amount = getMinusAmountInCents(request.user.order.order_option)
            pre_amount = Balance.objects.get(user = request.user).remaining_balance

            if pre_amount <= 0:
                Balance.objects.filter(user=request.user).update(is_valid=False)
                
            Balance.objects.filter(user=request.user).update(remaining_balance=pre_amount-amount)
            response = HttpResponse(content_type='text/json')
            print(results)
            response['results']=results


            return JsonResponse(results)
       
        else:
            response = HttpResponse(content_type='text/json')
            response['results']={'status'==409}
            return JsonResponse(results)


@login_required(login_url='login')
def getHiringDataByTextInput(request):
    
    if request.method == 'POST' :
        if request.user.balance.is_valid == True:
            keyword = request.POST.get('keyword')
            maxPages=5
            client = Client()
            keywords = keyword.split(',')
            print(keywords)
            try:
                results = client.search(keywords=keywords, location="New York", maxPages=int(maxPages))
            except:
                results={}
            print(results)
            amount = getMinusAmountInCents(request.user.order.order_option)
            pre_amount = Balance.objects.get(user = request.user).remaining_balance
            print('################################################################3')
            print('################################################################3')
            print('################################################################3')
            print(pre_amount)
            print('################################################################3')
            print('################################################################3')
            print('################################################################3')

            if pre_amount <= 0:             
                Balance.objects.filter(user=request.user).update(is_valid=False)
                
            Balance.objects.filter(user=request.user).update(remaining_balance=pre_amount-amount)
            response = HttpResponse(content_type='text/json')
            response['results']=results

            return JsonResponse(results)
        else:
            response = HttpResponse(content_type='text/json')
            response['results']={'status'==409}

            return JsonResponse(results)