import ssl
import json
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class Client:
    def __init__(self):
        pass

    def __parseDate(self, string):
        from datetime import datetime, timedelta

        try:
            days = int(string.split(" ")[0])
        except IndexError:
            return None
        except ValueError:
            if string == "Today":
                days = 0
            else:
                return None

        return datetime.strftime((datetime.now() - timedelta(days=days)), "%Y-%m-%d")

    def __parseURL(self, string):
        return "https://www.indeed.com%s" % string

    def __getResultsCount(self, html):
        # try:
            raw = html.find("div", {"id": "searchCountPages"}).text.strip()
            return int(raw.split(" ")[3].replace(",", ""))
        # except (AttributeError, IndexError, ValueError) as e:
        #     return None

    def __find(self, html, balise, name):
        try:
            return html.find(balise, {"class": name}).text.strip()
        except AttributeError:
            return None

    def search(self, keywords, location=None, company_name=None, maxPages=None):

        if not isinstance(keywords, list):
            raise TypeError("Keywords must be a list of string")

        if not len(keywords):
            raise IndexError("At least one keyword must be provided")

        safe_keywords = "+".join(
            ["+".join(str(e).lower().split(" ")) for e in keywords]
        )

        ssl._create_default_https_context = ssl._create_unverified_context

        ua = UserAgent(use_cache_server=False)

        resultsByPages, data = 10, list()
        endpoint = "https://www.indeed.com/jobs?q=%s" % safe_keywords
        print(endpoint)
        if location:
            safe_location = "+".join(location.lower().split(" "))
            endpoint += "&l=%s" % safe_location

        start = time.time()

        response = requests.get(endpoint, headers={"User-Agent": ua.random})
        soup = BeautifulSoup(response.text, "html.parser")
        
        resultsCount = self.__getResultsCount(soup)
        
        pageCount = resultsCount // resultsByPages

        if maxPages:
            pageCount = maxPages
        id=1
        for n in range(pageCount):
            response = requests.get(
                "%s&start=%s" % (endpoint, 10 * n), headers={"User-Agent": ua.random}
            )
            soup = BeautifulSoup(response.text, "html.parser")

            subSoup = soup.findAll("div", {"class": "result"})
            for element in subSoup:
                e = {
                    "id":id,
                    "title": self.__find(element, "div", "title"),
                    "location": self.__find(element, "span", "location"),
                    "url": self.__parseURL(
                        element.find("a", {"class": "jobtitle"})["href"]
                    ),
                    "company_name": self.__find(element, "span", "company"),
                    "company_rating": self.__find(element, "a", "ratingNumber"),
                    "keywords": keywords,
                    "creation_date": self.__parseDate(
                        self.__find(element, "span", "date")
                    ),
                }
                id+=1

                if company_name and (
                    company_name.lower() not in e["company_name"].lower()
                ):
                    continue

                data.append(e)

        return {
            "execution_time": time.time() - start,
            "count": {
                "pages": pageCount,
                "jobs": len(data),
                "companies": len(list(set([e["company_name"] for e in data]))),
            },
            "endpoint": endpoint,
            "data": data,
        }
