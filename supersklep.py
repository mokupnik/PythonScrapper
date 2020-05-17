import requests
from bs4 import BeautifulSoup
import urllib

class SuperSklepResult:
    def __init__(self, item_name, amount=3):
        self.item_name = item_name
        self.amount = amount
        self.assin_array = []
        self.items = {}
        self.error = 0


        self.url = 'https://supersklep.pl/catalog/page/products?keywords='
        for s in self.item_name:
            if s == ' ':
                self.url += '%20'
            else:
                self.url += s

        self.soup = self.make_soup(self.url)
        if (self.error == 0):
            self.get_assin()
            self.get_prices()

    def make_soup(self, url):
        try:
            page = urllib.request.urlopen(url)
        except:
            print('Ignored: ')
            self.error = 1
            return -1

        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urllib.request.urlopen(req).read()
        soup_data = BeautifulSoup(page, "html.parser")
        return soup_data

    def get_assin(self):
        for a in self.soup.findAll('a', href=True):
            if not isinstance(a,int):
                url = a['href']
                if len(url) > 22:
                    if url[22] == 'i' and url !='/certyfikaty#RzetelnaFirma':
                        self.assin_array.append(url)

    def get_prices(self):
        assin = self.assin_array[:self.amount]
        for a in assin:
            url = a
            new_soup = self.make_soup(url)
            price = list(new_soup.findAll('p')[1])[0]
            name = list(new_soup.findAll('h1')[0])[0]
            self.items[name] = price



