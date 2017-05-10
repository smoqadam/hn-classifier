from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from aylienapiclient import textapi


def index(request):
    client = textapi.Client("APP_ID","APP_KEY")
    hr = requests.get('https://news.ycombinator.com/')

    html = BeautifulSoup(hr.content, 'html.parser')
    links = html.find_all('a', class_="storylink")
    categories = dict()
    for (i, link) in enumerate(links):
        href = link.get('href')
        p = client.Classify({'url': href})
        try:
            label = p['categories'][0]['label']
            if label in categories:
                categories[label].append((link.get_text(), href))
            else:
                categories[label] = [(link.get_text(), href)]
        except:
            print(p)
    
    return render(request, 'hr/index.html',{'c':categories})