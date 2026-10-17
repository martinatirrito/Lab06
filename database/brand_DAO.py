from database.DB_connect import DBConnect


class brand_DAO:
    @staticmethod
    def getBrand():
        try:
            conn = DBConnect.get_connection()  # me lo scrivo uguale a sopra nell'import
            cursor = conn.cursor(dictionary=True)

        except ConnectionError:
            print("Errore di connessione al databse")
            return

        query = """select distinct gp.Product_brand as brand
                    from go_products gp """

        cursor.execute(query, )
        res = []
        for row in cursor:
            if row["brand"] is not None:
                res.append(row["brand"])

        cursor.close()
        conn.close()

        return res