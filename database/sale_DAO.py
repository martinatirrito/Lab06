from database.DB_connect import DBConnect
from model.sale import Sale


class sale_DAO:
    @staticmethod
    def getAnno():
        try:
            conn = DBConnect.get_connection() # me lo scrivo uguale a sopra nell'import
            cursor = conn.cursor(dictionary=True)

        except ConnectionError:
            print("Errore di connessione al databse")
            return

        query = """select distinct year (gds.date) AS anno
                    from go_daily_sales gds """
        cursor.execute(query,)
        res = []
        for row in cursor:
            if row["anno"] is not None:
                res.append(row["anno"])

        cursor.close()
        conn.close()

        return res

    def getFilteredSales(anno, brand, codice):
        # ritorna le vendite con il ricavo più alto in base ai filtri selezionati
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select gds.retailer_code, gds.product_number, gds.date, (gds.unit_sale_price*gds.quantity) as ricavo 
                            from go_daily_sales gds, go_products gp, go_retailers gr 
                            where gds.product_number=gp.product_number 
                                    and	gds.retailer_code=gr.retailer_code 
                                    and gds.retailer_code=coalesce(%s, gds.retailer_code)  #coalesce?
                                    and gp.product_brand=coalesce(%s, gp.product_brand)
                                    and year(gds.date)=coalesce(%s, year(gds.date))
                            order by ricavo desc"""
       #POTEVO SCRIVERE LIMIT 5 PRENDO LE PRIME CINQUE CON SQL
        # con il comando coalesce, se passo come parametro un None l'istruzione viene semplicemente ignorata e si passa avanti

        cursor.execute(query, (codice, brand, anno,))

        res = []
        for row in cursor:
            res.append(Sale(**row))

        cursor.close()
        cnx.close()

        return res