import requests
from bs4 import BeautifulSoup
import urllib

class BludshopResult:

    def __init__(self, item_name, amount=3):
        self.item_name = item_name
        self.amount = amount
        self.assin_array = []
        self.items = {}
        self.error = 0



        self.url = 'https://bludshop.com/search.php?text='
        for s in self.item_name:
            if s == ' ':
                self.url += '+'
            else:
                self.url += s

        self.soup = self.make_soup(self.url)

        if(self.error==0):
            self.get_assin()
            self.get_prices()


    def make_soup(self, url):
        try:
            page = urllib.request.urlopen(url)
        except:
            self.error = 1
            return -1


        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urllib.request.urlopen(req).read()
        soup_data = BeautifulSoup(page, "html.parser")
        return soup_data

    def get_assin(self):
        for a in self.soup.findAll('a', href=True):
            url = a['href']
            if url[1:8] == 'product' and url not in self.assin_array:
                self.assin_array.append(url)

    def get_prices(self):
        assin = self.assin_array[:self.amount]
        for a in assin:
            url = 'https://bludshop.com/' + a
            new_soup = self.make_soup(url)
            price = new_soup.find(id='projector_price_value').get_text()[:5]
            self.items[a[19:-5]] = price


