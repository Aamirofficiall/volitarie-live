from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from .scrapData import *
import csv
import io
        
# client = TrustRadius.Client()
# results = client.getReviews(keyword='Asana',  maxPages=1)
def getHiringData(request):
    
    if request.method == 'POST' and request.FILES['file']:
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
        response = HttpResponse(content_type='text/json')
        print(results)
        response['results']=results

        return JsonResponse(results)



def index(request): 
    return render(request, 'competition.html')


def getCompetitionData(request):

    if request.method == 'POST' and request.FILES['file']:
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            response = HttpResponse(content_type='text/json')
            response['notCSV'] = True
            return  response

        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        keyword=[]
        maxPages=''
        
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                keyword.append(column[0]) 
        print('#################################################')
        print(keyword)
        print('#################################################')
        client = Client()

        # calling the scrapper to provide u data

        # for key in keyword:
            
        results = client.getReviews(
            keyword='illustrator',  maxPages=2)
        
        try:
            results[key].append(client.search(keywords=keyword, location="New York", maxPages=int(maxPages)))
        except:
            
            results[key].append({})

        print(results)
        response = HttpResponse(content_type='text/json')
        response['results']=results

        return JsonResponse(results)

def getCompetitionDataByTextInput(request):
    
    if request.method == 'POST' :
        keyword = request.POST.get('keyword')
        maxPages=5
        client = Client()

        try:
            results = client.search(keywords=keyword,maxPages=int(maxPages))
        except:
            results={}
        print(results)
        response = HttpResponse(content_type='text/json')
        response['results']=results

        return JsonResponse(results)


