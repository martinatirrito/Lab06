import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Lab-06"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # 1. Titolo
        self._title = ft.Text("Analizza Vendite", color="blue", size=24)
        self._page.controls.append(self._title)

        # PRIMA RIGA DROPDOWN
        self.dd_anno = ft.Dropdown(
            width=200,
            hint_text="Filtro per anno",
            label="anno",
            options=[ft.dropdown.Option(key="None", text="Nessun filtro")],
            on_change=self._controller.read_anno #?????
        )

        self.dd_brand = ft.Dropdown(label="brand", width=300,
                                    options=[ft.dropdown.Option("Nessun filtro")])

        self.dd_retailer = ft.Dropdown(label="retailer", expand=True,  # prende tutto lo spazio rimasto sulla riga
                                       options=[ft.dropdown.Option("Nessun filtro")])

        # 3. Creazione della riga con i tre dropdown e aggiunta alla pagina
        row1= ft.Row([self.dd_anno, self.dd_brand, self.dd_retailer], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

       #SECONDA RIGA BOTTONI
        self.btn_top_sales = ft.ElevatedButton(text="Top vendite", on_click=self._controller.handle_top_sales)
        self.btn_analizza = ft.ElevatedButton(text="Analizza vendite", on_click=self._controller.handle_analizza)

        row2 = ft.Row([self.btn_top_sales, self.btn_analizza], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)


        # 5. ListView per stampare i risultati
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

        #popolo solo alla fine
        self._controller.fillDDAnno()
        self._controller.fillDDBrand()
        self._controller.fillDDRetailer()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
