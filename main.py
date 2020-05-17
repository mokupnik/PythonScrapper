from bs4 import BeautifulSoup
import bludshop as bd
import supersklep as sp
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import gui as gui
import requests
import vtr as vtr
import concurrent.futures

class FirstWindow(Gtk.Window):
    # klasa pierwszego okna, po nacisnieciu Search - pobieramy text - chyba ze nic nie wpisalismy (czyli tak jak domyslnie, widnieje 'Item')
    def __init__(self):
        Gtk.Window.__init__(self, title="Ceneo")
        self.text = ''
        self.set_border_width(10)
        self.set_size_request(200,100)

        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 8)
        self.add(vbox)

        self.search = Gtk.Entry()
        self.search.set_text('Item')
        self.button = Gtk.Button(label='Search')
        self.button.connect('clicked', self.search_for)
        vbox.pack_start(self.search, True, True, 0)
        vbox.pack_start(self.button, True, True, 0)

    def make_object_sp(self):
        return lambda x: sp.SuperSklepResult(x)

    def make_object_bd(self):
        return lambda x: bd.BludshopResult(x)

    def make_object_vtr(self):
        return lambda x: vtr.VtrResult(x)

    def search_for(self, widget):
        # pobranie textu z wejscia i sprawdzenie czy cos wpisaliśmy.
        self.text = self.search.get_text()
        if self.text != 'Item':
            lista = []

            ## Wielowatkowosc - stworzenie obiektow zdefiniowanych w odpowiadajych im modulach
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                future_soup_sp = executor.submit(self.make_object_sp(), self.text)
                future_soup_bd = executor.submit(self.make_object_bd(), self.text)
                future_soup_vtr = executor.submit(self.make_object_vtr(), self.text)

            soup_sp = future_soup_sp.result()
            soup_bd = future_soup_bd.result()
            soup_vtr = future_soup_vtr.result()

            for i in soup_sp.items.keys():
                lista.append([i, float(soup_sp.items[i][0:-7]),'Supersklep']) ## pozbywam się niepotrzebnych znaków koło cen (np. PLN etc) oraz zamieniwam na floaty
            for j in soup_bd.items.keys():                                     # oraz zmieniam słowniki które dostałem, na jedna dlugą liste list : Nazwa,Cena,Sklep
                lista.append([j, float(soup_bd.items[j][0:-2]), 'Bludshop'])
            for k in soup_vtr.items.keys():
                lista.append([k, float(soup_bd.items[j][:-2]), 'VtrShop'])
            lista.sort(key=lambda x:x[1]) # sortuje liste list  wzgledem ceny
            noteb = gui.NotebookTabbed(lista,self.text)
            noteb.show_all()



app = FirstWindow()
app.show_all()
app.connect('delete-event',Gtk.main_quit)
app.show_all()
Gtk.main()
app.destroy()
