import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
text_input = ''




class NotebookTabbed(Gtk.Window):

    def __init__(self, lista, text):
        Gtk.Window.__init__(self, title='Steal Alert')
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)
        self.lista = lista
        self.results = Gtk.Box()
        self.text = text

        ## implementacja wyświetlanie listy ofert za pomocą Gtk.TreeView i Gtk.Notebook
        store_lista = Gtk.ListStore(str, int, str)
        for item in self.lista:
            store_lista.append(list(item))

        store_tree_view = Gtk.TreeView(store_lista)

        for i, col_title in enumerate(['Nazwa', 'Cena', 'Sklep']):

            renderer = Gtk.CellRendererText()

            column = Gtk.TreeViewColumn(col_title,renderer,text=i)

            store_tree_view.append_column(column)


        # tworzymy 'druga strone' okienka, dodatkow informację

        info_lista = Gtk.ListStore(str, str)
        info_lista.append(['Info', 'Projekt na Rozszerzony Kurs Pythona'])
        info_lista.append(['Github: ', 'MOku98'])
        info_lista.append(['Wyniki dla: ', self.text])

        info_tree_lista = Gtk.TreeView(info_lista)

        column = Gtk.TreeViewColumn('Atrybut', renderer, text=0)
        info_tree_lista.append_column(column)
        column = Gtk.TreeViewColumn('Nazwa', renderer, text=1)
        info_tree_lista.append_column(column)

        self.analize = Gtk.Box()
        self.results.add(store_tree_view)
        self.analize.add(info_tree_lista)
        self.notebook.append_page(self.results, Gtk.Label('Oferty'))
        self.notebook.append_page(self.analize, Gtk.Label('Info'))



