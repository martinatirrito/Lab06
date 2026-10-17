from database.DB_connect import DBConnect
from model.retailer import Retailer


class retailer_DAO:
    @staticmethod
    def getRetailer():
        try:
            conn = DBConnect.get_connection()  # me lo scrivo uguale a sopra nell'import
            cursor = conn.cursor(dictionary=True)

        except ConnectionError:
            print("Errore di connessione al databse")
            return

        query = """select distinct gr.retailer_code , gr.retailer_name, gr.type, gr.country
                    from go_retailers gr 
                    order by retailer_name"""

        cursor.execute(query, )
        res = []
        for row in cursor:
            res.append(Retailer(**row))

        cursor.close()
        conn.close()

        return res