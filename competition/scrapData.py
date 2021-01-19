import requests
import csv
import json
import time
import ssl
from pprint import pprint
from bs4 import BeautifulSoup
from textblob import TextBlob
import random
import urllib


class Client:
    def __init__(self):
        pass

    def __find(self, html, balise, name):
        try:
            return html.find(balise, {"class": name}).text.strip()
        except AttributeError:
            return None

    def __extractIndustry(self, string):
        try:
            return string.split(',')[0].strip()
        except AttributeError:
            return None

    def __extractCompanySize(self, string):
        try:
            return string.split(',')[1].strip()
        except (AttributeError, IndexError) as e:
            return None

    def __extractScore(self, string):
        try:
            return string.replace('Score\xa0', '').split(' ')[0]
        except AttributeError:
            return None

    def __extractAttributes(self, html, name):
        result = list()
        atts = html.find('ul', {'class': name})

        if atts:
            result = [att.text for att in atts]

        return result

    def __getResultsCount(self, html):
        try:
            text = html.find('div', {'id': 'product_reviews'}).find(
                "span", {"class": "counts"}).text
            return int(text.split(' ')[-1].replace(')', ''))
        except AttributeError:
            return None
        except ValueError:
            return None

    def __extractURL(self, html):
        try:
            return 'https://www.trustradius.com' + html.find('a', {"class": 'url'})['href']
        except TypeError:
            return None

    def __getReviewURL(self, keyword):
        search_url = 'https://www.trustradius.com/search?q=%s' % urllib.parse.quote(
            keyword.lower().strip())

        response = requests.get(search_url, headers={
                                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130330 Firefox/21.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        product_links = [product['href']
                         for product in soup.findAll('a', {'class': 'product-link'})]

        if not product_links:
            raise TypeError("Product not found")

        return 'https://www.trustradius.com' + product_links[0]

    def getReviews(self, keyword, maxPages=None):

        endpoint = self.__getReviewURL(keyword)

        start = time.time()

        headers = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130330 Firefox/21.0",
                   "Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3",
                   "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                   "Opera/9.80 (Windows NT 6.1; U; ko) Presto/2.7.62 Version/11.00",
                   "Opera/9.80 (Windows NT 6.1 x64; U; en) Presto/2.7.62 Version/11.00"]

        results_by_pages = 25

        response = requests.get(
            endpoint, headers={"User-Agent": random.choice(headers)})
        soup = BeautifulSoup(response.text, "html.parser")

        subSoup = soup.findAll("div", {"class": "serp-row"})

        results = list()

        result_count = self.__getResultsCount(soup)
        page_count = result_count // results_by_pages

        if maxPages and isinstance(maxPages, int):
            page_count = maxPages
        id=1

        for n in range(page_count):
            url = endpoint + '?f=%s' % (results_by_pages * n)

            response = requests.get(
                url, headers={"User-Agent": random.choice(headers)})
            soup = BeautifulSoup(response.text, "html.parser")

            subSoup = soup.findAll("div", {"class": "serp-row"})

            for element in subSoup:
                review = element.find('h3', {"class": "review-title"})

                if not review:
                    continue

                data = {
                    "id":id,
                    'title': review.text,
                    'createdAt': self.__find(element, 'div', 'review-date'),
                    'reviewer_name': self.__find(element, 'div', 'name'),
                    'reviewer_position': self.__find(element, 'div', 'position'),
                    'reviewer_company': self.__find(element, 'span', 'company'),
                    'reviewer_company_size': self.__extractCompanySize(self.__find(element, 'span', 'industry')),
                    'reviewer_industry': self.__extractIndustry(self.__find(element, 'span', 'industry')),
                    'reviewer_url': self.__extractURL(element),
                    'trust_score': self.__extractScore(self.__find(element, 'div', 'trust-score__score')),
                    'use_cases': None,
                    'attributes': {
                        'pros': [],
                        'cons': []
                    },
                    'likelihood_to_recommend': None,
                    'analysis': {
                        'polarity': None,
                        'subjectivity': None
                    }
                }

                questions = element.findAll(
                    "div", {"class": "question-display-box"})

                for question in questions:
                    question_title = self.__find(
                        question, 'h3', 'question-title')

                    if question_title == 'Use Cases and Deployment Scope':
                        data['use_cases'] = self.__find(question, 'div', 'ugc')

                    if question_title == 'Pros and Cons':
                        for n in ['pros', 'cons']:
                            data['attributes'][n] = self.__extractAttributes(
                                question, n)

                    if question_title == 'Likelihood to Recommend':
                        data['likelihood_to_recommend'] = self.__find(
                            question, 'div', 'ugc')

                if data['likelihood_to_recommend']:
                    likelihood = TextBlob(data['likelihood_to_recommend'])
                    data['analysis']['polarity'] = round(
                        likelihood.sentiment.polarity, 3)
                    data['analysis']['subjectivity'] = round(
                        likelihood.sentiment.subjectivity, 3)
                id+=1

                results.append(data)

        return {
            "execution_time": time.time() - start,
            "reviews_count": len(results),
            "endpoint": endpoint,
            "data": results
        }
