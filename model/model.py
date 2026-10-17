from database.brand_DAO import brand_DAO
from database.DAO import DAO
from database.retailer_DAO import retailer_DAO
from database.sale_DAO import sale_DAO


class Model:
    def __init__(self):
        pass

    #recuper dati dal dao
    def getAnno(self):
        return sale_DAO.getAnno()    #prendo dal database con il DAO

    def getBrand(self):
        return brand_DAO.getBrand()

    def getRetailer(self):
        return retailer_DAO.getRetailer()

#???
    def getFilteredSales(self, anno, brand, codice):
        if anno == "Nessun filtro":
            anno = None
        if brand == "Nessun filtro":
            brand = None
        if codice == "Nessun filtro":
            codice = None
            # passa None se non c'è filtro in modo da nno crashare la query sql dopo
        return DAO.getFilteredSales(anno, brand, codice)

