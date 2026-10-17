import flet as ft   #prova

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    #DROPDOWN ANNO
    def fillDDAnno(self):
        """methodo che popola la tendina con tutti gli anni in cui ci sono state vendite,
               prendendo le informazioni dal database"""
        anni = self._model.getAnno() #prendo anni dal database con la funzione che scrivo nel model
        #anniOption = list(map(lambda x: ft.dropdown.Option(anni)))  #??? devo mettere key o qualcosa??
        for anno in anni:
            self._view.dd_anno.options.append(ft.dropdown.Option(str(anno)))
        self._view.update_page()

    def read_anno(self, e):
        """event handler che legge l'anno scelto dal menu a tendina ogniqualvolta viene cambiata
        la scelta, e lo memorizza in una variabile di instanza. L'anno è un intero, se si tratta di un anno,
        oppure un None se viene scelta l'opzione nessun filtro sull'anno"""
        #copiato
        #usato quando nel dropdown ho un oggetto
        if e.control.value == "None":
            self._anno = None
        else:
            self._anno = e.control.value

    #DROPDOWN BRAND
    def fillDDBrand(self):
        brands = self._model.getBrand()
           #for brand in brands:
            #self._view.dd_anno.options.append(ft.dropdown.Option(str(brand)))
            #self._view.update_page()
        brands.sort()
        for brand in brands:
            self._view.dd_brand.options.append(ft.dropdown.Option(key=brand,text=brand))
        self._view.update_page()

    #DROPDOWN RETAILER
    def fillDDRetailer(self):
        retailers = self._model.getRetailer()
        retailers.sort(key=lambda x: x.retailer_name)
        for ret in retailers:
            self._view.dd_retailer.options.append(
                ft.dropdown.Option(
                    key=ret.retailer_code,  #chiave id
                    text=ret.retailer_name, #
                    data=ret,
                    on_click=self.read_retailer  # handler per leggere l'oggetto selezionato
                )
            )
            self._view.update_page()

    #COPIATO
    def read_retailer(self, e):
        self._retailer = e.control.data  # cioè l'oggetto selezionato dall'esterno
        #e collegato al mio on click, faccio .data perchè la data dell'opzione è il mio oggetto retailer,
                                            #così quando me lo richiamo lo passo come parametro al modello usando l'OGGETTO

    #SECONDA RIGA BOTTONI
    def handle_top_sales(self, e):
        self._view.txt_result.controls.clear()

        #filtro se non ho selezionato niente
        if self._view.dd_anno.value is None or self._view.dd_brand.value is None or self._view.dd_retailer.value is None:
            self._view.create_alert("Attenzione! Selezionare filtri")
            return

        #
        sales = self._model.getFilteredSales(self._view.dd_anno.value, self._view.dd_brand.value, self._view.dd_retailer.value)
        stop = min(len(sales), 5)

        #voglio le migliori 5 vendite
        if stop == 0:
            self._view.txt_result.controls.append(
                ft.Text("Non ci sono vendite che corrispondono ai filtri selezionati",
                        color="blue")
            )
            self._view.update_page()
            return

        #?????
        if self._view.dd_anno.value == "Nessun filtro" and self._view.dd_brand.value == self._view.dd_retailer.value and self._view.dd_anno.value == self._view.dd_brand.value:
            # cioè se selezioniamo sempre Nessun filtro:
            self._view.txt_result.controls.append(
                ft.Text(f"Ecco le prime 5 vendite del database, in ordine di ricavo:"))
        else:
            self._view.txt_result.controls.append(
                ft.Text(f"Ecco le prime {stop} vendite che corrispondono ai filtri selezionati, in ordine di ricavo:"))
        i = 0
        while i < stop:
            self._view.txt_result.controls.append(
                ft.Text(f"{sales[i]}")
            )
            i += 1
        self._view.update_page()


    def handleAnalisiVendite(self, e):
        self._view.txt_result.controls.clear()
        if self._view.dd_anno.value is None or self._view.dd_brand.value is None or self._view.dd_retailer.value is None:
            self._view.create_alert("Attenzione! Selezionare filtri")
            return

        vendite = self._model.getFilteredSales(self._view.dd_anno.value, self._view.dd_brand.value,
                                               self._view.dd_retailer.value)
        affari=0  #SOMMA RICAVI VENDITE FILTRATE
        retailers=set() #creo un set, in modo da non avere elementi duplicati
        prodotti=set()
        if len(vendite)==0:
            self._view.txt_result.controls.append(
                ft.Text("Non ci sono vendite che corrispondono ai filtri selezionati",
                        color="blue")
            )
            self._view.update_page()
            return
        for v in vendite:
            affari+=v.ricavo
            retailers.add(v.retailer_code)
            prodotti.add(v.product_number)
        self._view.txt_result.controls.extend( #aggiunge più di un elemento contemporaneamente alla lista
            [ft.Text("Statistiche vendite:"),
             ft.Text(f"Giro d'affari: {affari}"),
             ft.Text(f"Numero vendite: {len(vendite)}"),
             ft.Text(f"Numero retailers coinvolti: {len(retailers)}"),
             ft.Text(f"Numero prodotti coinvolti: {len(prodotti)}")])
        self._view.update_page()


