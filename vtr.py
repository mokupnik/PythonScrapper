import requests
from bs4 import BeautifulSoup
import urllib

class VtrResult:

    def __init__(self, item_name, amount=3):
        self.item_name = item_name
        self.amount = amount
        self.assin_array = []
        self.items = {}

        self.url = 'https://vtrn.pl/search.php?text='
        for s in self.item_name:
            if s == ' ':
                self.url += '+'
            else:
                self.url += s # tworzenie pierwszego linku

        self.soup = self.make_soup(self.url)
        self.get_assin()
        self.get_prices()

    def make_soup(self, url):
        try:
            page = urllib.request.urlopen(url)
        except urllib.request.HTTPError as e:
            print('Ignored: ', e)
            return -1

        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urllib.request.urlopen(req).read()
        soup_data = BeautifulSoup(page, "html.parser")
        return soup_data

    #pobranie wszystkich poprawnych linków (a w zasadzie tym co wysteepuje po stronie glownej sklepu) z listy wyszukanych produktow
    def get_assin(self):
        if not isinstance(self.soup,int):
            for a in self.soup.findAll('a', href=True):
                url = a['href']
                if url[1:8] == 'product' and url not in self.assin_array:
                    self.assin_array.append(url)
        else:
            self.amount=0

    def get_prices(self):
    #przechodzimy przez pobrane linki, tworzymy poprawny adres  dodajac vtrn.pl, oraz sciagamy cene
        assin = self.assin_array[:self.amount]
        for a in assin:
            url = 'https://vtrn.pl' + a
            new_soup = self.make_soup(url)
            price = new_soup.find(id='projector_price_value').get_text()[:5]
            self.items[a[19:-5]] = price # items to słownik items[nazwa_produktu] = cena
