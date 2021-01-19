
from linkdin.linkedInScrapper import constructEmailTemplate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from payment.models import * 
import csv
import io



email = 'ahsan44411@gmail.com'
password = 'pakistane12345'
profile_url = 'https://www.linkedin.com/in/icaspi/'



def getMinusAmountInCents(string):
    if string == 'Starter':
        return 0.198 *100
    elif string == 'Pro':
        return 0.165*100
    elif string == 'Enterprise':
        return  0.142  *100



def index(request):

    return render(request, 'linkdin.html')

@login_required(login_url='login')
def getLinkdinData(request):

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

            print('###############################')
            print('###############################')
            print(keyword)
            print('###############################')
            print('###############################')

    
            # keyword.pop(0)
            try:
                results={}
                data=[]
                for profile_url in keyword:
                    print(profile_url)
                    goodies = constructEmailTemplate(email, password,profile_url)   
                    data.append(goodies)
            except: 
                results={}
            #####################################################################################################
            # ########################################### Balance Part ##########################################
            #####################################################################################################

            amount = getMinusAmountInCents(request.user.order.order_option)
            pre_amount = Balance.objects.get(user = request.user).remaining_balance
            if pre_amount <= 0.0:
                Balance.objects.filter(user=request.user).update(is_valid=False)
            Balance.objects.filter(user=request.user).update(remaining_balance=pre_amount-amount)

            response = HttpResponse(content_type='text/json')
            response['results']=results
            results['data']=data
            print(results)

            return JsonResponse(results)
       
        else:
            response = HttpResponse(content_type='text/json')
            response['results']={'status'==409}
            results={}
            return JsonResponse(results)
    
    response = HttpResponse(content_type='text/json')
    response['results']={'status'==409}
    return JsonResponse(response,safe=False)

