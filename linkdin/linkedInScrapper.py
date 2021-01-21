import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import datetime
import random
import operator
from GoogleNews import GoogleNews
from newspaper import Article
import pandas as pd
from newspaper import fulltext
import os


PATH = os.path.realpath('finalized_model.sav')

def get_html(email, password, profile):
    client = requests.Session()

    HOMEPAGE_URL = 'https://www.linkedin.com/'
    LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'
    CONNECTIONS_URL = 'https://www.linkedin.com/mynetwork/invite-connect/connections/'

    html = client.get(HOMEPAGE_URL).content
    soup = BeautifulSoup(html, 'lxml')
    csrf = soup.find('input', dict(name='loginCsrfParam'))['value']

    login_information = {
        'session_key': email, #'ahsan44411@gmail.com',
        'session_password': password, #'pakistane12345',
        'loginCsrfParam': csrf,
    }
    try:
        client.post(LOGIN_URL, data=login_information)
        print("Login Successful")
    except:
        print("Failed to Login")

        
    html = client.get(profile).content
    soup = BeautifulSoup(html , "html.parser")
    
    
    posts_urls = profile+'/detail/recent-activity/posts/'
    html = client.get(posts_urls).content #opens ASPIRING_DATA_SCIENTIEST
    post_soup = BeautifulSoup(html , "html.parser")
    
    return soup, post_soup



def get_info(soup):
    
    codes = soup.find_all('code')
    
    schools = {}
    position = {}
    company = ''
    location = {}
    city = ''
    name = ''
    
    for code in codes:
        try:
            for data in code.children:
                res = json.loads(data[3:len(data)-1])
                for ele in res['included']:
                    try:
                        pass
                    except:
                        pass 
                    try:
                        city = ele['defaultLocalizedNameWithoutCountryName']
                    except:
                        pass                 
                    try:
#                         print('multiLocaleTitle',ele['multiLocaleTitle'])
                        pass
                    except:
                        pass
                    try:
#                         print('multiLocaleHeadline',ele['multiLocaleHeadline'])
                        try:
                            headline = ele['multiLocaleHeadline']['en_US'].split('|')
                            position = headline[0].split('at')[0]
                            company = headline[0].split('at')[1]
                        except:
                            pass
                    except:
                        pass
                    try:
                        pass
#                         print('multiLocaleLastName',ele['multiLocaleLastName'])
                    except:
                        pass
                    try:
#                         print('multiLocaleFirstName',ele['multiLocaleFirstName'])
                        try:
                            name = ele['multiLocaleFirstName']['en_US']
                        except:
                            pass
                    except:
                        pass
                    try:
#                         print('multiLocaleSchoolName',ele['multiLocaleSchoolName'])
                        pass
                        try:
#                             print(ele['dateRange']['end']['year'])
                            schools[ele['multiLocaleSchoolName']['en_US']] = ele['dateRange']['end']['year']
                        except Exception as e:
                            pass
                    except:
                        pass                
        except:
            pass
    return schools, position, company, location, city, name





# weather
def weatherSearch(city):
    url = "https://community-open-weather-map.p.rapidapi.com/weather"
    querystring = {
        "q": "{}".format( city )
        }
    headers = {
    "x-rapidapi-host": "community-open-weather-map.p.rapidapi.com",
    "x-rapidapi-key": "3ee9617d65mshde7711079b6ec96p170845jsn4aa64d62b209"
    }
    rapid = requests.request("GET", url, headers=headers, params=querystring)

    x = rapid.json()
    if x["cod"] != "404": 
        y = x["main"] 
        current_temperature = y["temp"] 
        current_pressure = y["pressure"] 
        current_humidiy = y["humidity"] 
        z = x["weather"] 
        weather_description = z[0]["description"] 
    else: 
        print("City Not Found")
        return "City Not Found"
    return {'temp celsius':current_temperature - 273.15, 'weather_description':weather_description}


def constructWeather(city):
    weatherdata = weatherSearch(city)
    
    if weatherdata == "City Not Found":
        return 'hope you had a chance to enjoy the weather in '+ city

    if weatherdata['temp celsius'] < 15 and weatherdata['temp celsius'] > 5:
        weather15_5 = ["How the weather there these days? Hope you're warm and cozy", 
                             "Hows the weather in <place>. Its cold here."]
        return random.choice(weather15_5).replace("<place>", city)

    elif weatherdata['temp celsius'] < 0:
        weather_0 = ["How the weather there these days? Hope you're warm and cozy", 
                     "Hows the weather in <place>. Its cold and freezing here."]
        return random.choice(weather_0).replace("<place>", city)

    elif 'fog' in weatherdata['weather_description'] or 'smoke' in weatherdata['weather_description']:
        fog_smoke = ["Heard about the dense smog/ fog in <place>, hope you're driving safely.", 
                     "hope your safe from the dense fog in <place>"]
        return random.choice(fog_smoke).replace("<place>", city)

    elif 'heavy intensity rain' in weatherdata['weather_description']:
        heavy_rain = ["Hope you are safe from the massive rain in <place>."]
        return random.choice(heavy_rain).replace("<place>", city)


    elif 'rain' in weatherdata['weather_description'] or 'slight rain' in weatherdata['weather_description']:
        rain = ["It rained today in <place>. Hope you have a chance to enjoy the weather."]
        return random.choice(rain).replace("<place>", city)
    
    dt = datetime.datetime.today()

    if dt.month>3 and dt.month<5:
        spring = ["Hows the weather there these days? Heard it gets really beautiful this time of the year.",
                            "Did you have the chance to enjoy the beautiful weather today."]
        return random.choice(spring).replace("<place>", city)
    
    else:
        default = 'hope you had a chance to enjoy the good weather in '+ city
        return default
    
def constructUniversity(schools):
    university = ['It is an honour to talk to another alumi from <university>',
                 'Its always great to talk to another alumi of <university>',
                 'Its always great to talk to an alumi of <university>',
                 'Always great to talk to alumi of <university>',
                 'Great to talk to alumni of <university>']

    latestSchool = max(schools.items(), key=operator.itemgetter(1))[0]

    return random.choice(university).replace('<university>', latestSchool)

# Signature
def constructsignature():
    signature = [
    "Either way keep up the awesome work.",
    "Either way excited to see what you'll do this year",
    "Either way I am a big fan of your team",
    "Either way keep up the good work.",
    "Either way your doing awesome work.",
    "Either way love what you are doing.",
    "Either way big fan of your work.",
    "Either way. I am passionate about the work you do as much as you are. Keep on the good work."]
    return random.choice(signature)

# CTA
def constructCTA():
    CTA =['Will it be ridicoulous idea for you to explore any other solutions beyond what you are currently using? If I strike out I promise to never contact you again.',
    'Would you be against learning how we could be a potential resource for you? If I strike out I promise to me out of your inbox forever',
    'If you give me a shot I promise I will not jam your inbox with follow ups',
    'If you give me a chance to unpack how we can be relevant I promise you get some great value out of our conversation',
    'See how <Product> works. This is sure to add profit and value to your business.',
    '<Product> is very powerful. Explore how it can be useful to you.',
    'Im reaching out to talk to you about <product name>. Do not miss this opportunity to not use this <product>.',
    'Please take some time to talk about <product> which will boost your <> business',
    'I do not reach out until I am absolutly sure and passiante about <product>.']

    return random.choice(CTA)

def get_news(company):
    title = []
    summary = []
    
    googlenews=GoogleNews()
    
    googlenews.search(company)
    
    result=googlenews.result()
    df=pd.DataFrame(result)
    news = {}
    try:
        for link in df['link']:
            try:
                article = Article(link)
                article.download()
                article.parse()
                article.nlp()
                if str.lower(company) in str.lower(article.title):
#                     print(article.title)
#                     print(article.summary)
                    title.append(article.title)
                    summary.append(article.summary)
                    break
            except Exception as e:
                pass
    except:
        return title, summary
                
    return title, summary


import pickle

def getIndustry(JobTitle):

    filename = PATH
    sgd = pickle.load(open(filename, 'rb'))
    return sgd.predict([JobTitle])[0]

def postAndActivities(post_soup):

    link=''
    title=''
    summary = ''
    codes = post_soup.find_all('code')

    for code in codes:
        try:
            for data in code.children:
                data = data
            res = json.loads(data[3:len(data)-1])
            for ele in res['included']:
                try:
                    link = ele['permaLink']
                    title = ele['title']
                    
                    article = Article(link)
                    article.download()
                    article.parse()
                    article.nlp()
                    
                    summary = article.summary

                    return link, title, summary
                except:
                    pass
        except:
            pass
    return '','',''
    

def constructEmailTemplate(email, password, profile_url):

    soup, post_soup = get_html(email, password, profile_url)
    
    school, position, company, location, city, name = get_info(soup)
    
    post_link, post_title, post_summary = postAndActivities(post_soup)
    
    goodies = {'name':name, 'profile_url':profile_url, 'school':school, 'job_position': position, 'company': company, 'industry':getIndustry(position), 'location':city}
    
    goodies['weather'] = constructWeather(city)
    goodies['school'] = constructUniversity(school)
    
    goodies['intro_title_to_post'] = post_title
    goodies['intro_summary_to_post'] = post_summary
    goodies['intro_link_to_post'] = post_link

    goodies['news'] = get_news(company)
    title, summary = get_news(company)
    goodies['news title'] = title
    goodies['summay'] = summary
    goodies['CTA'] = constructCTA()
    goodies['signature_outro'] = constructsignature()
    
    
    return goodies





