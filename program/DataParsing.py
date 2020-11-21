import json
import os
import Product

class DataParsing:
    def __init__(self):
        self.store_records = {}

        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        script_dir += "\productData"
        product_files = [pos_json for pos_json in os.listdir(script_dir) if pos_json.endswith('.json')]
        print(product_files)

        for product_file in product_files:
            abs_file_path = os.path.join(script_dir, product_file)
            with open(abs_file_path, 'rb') as f:
                data = json.load(f)
            
            productList = []
            for product in data:
                productObj = self.parseData(product)
                productList.append(productObj)

            self.store_records[product_file] = productList

    def parseExchangeList(self, aList):
        exchangeListObj = Product.ProductUnitExchangeList()
        exchangeListObj.productUnitName = aList["productUnitName"]
        exchangeListObj.productUnitTxtUid = aList["productUnitTxtUid"]
        exchangeListObj.id = aList["id"]
        exchangeListObj.userId = aList["userId"]
        exchangeListObj.productUid = aList["productUid"]
        exchangeListObj.productUnitUid = aList["productUnitUid"]
        exchangeListObj.exchangeQuantity = aList["exchangeQuantity"]
        exchangeListObj.isBase = aList["isBase"]
        exchangeListObj.enable = aList["enable"]
        exchangeListObj.isRequest = aList["isRequest"]
        exchangeListObj.unitQuantity = aList["unitQuantity"]
        exchangeListObj.baseUnitQuantity = aList["baseUnitQuantity"]
        return exchangeListObj

    def parseData(self, productData):
        product = Product.Product()

        product.category_id = productData["category"]["id"]
        product.category_uid = productData["category"]["uid"]
        product.category_name = productData["category"]["name"]
        product.category_enable = productData["category"]["enable"]
        product.category_createdDatetime = productData["category"]["createdDatetime"]
        product.category_updatedDatetime = productData["category"]["updatedDatetime"]

        product.category_parent_id = productData["category"]["parent"]["id"]
        product.category_parent_uid = productData["category"]["parent"]["uid"]
        product.category_parent_name = productData["category"]["parent"]["name"]
        product.category_parent_enable = productData["category"]["parent"]["enable"]
        product.category_parent_createdDatetime = productData["category"]["parent"]["createdDatetime"]
        product.category_parent_updatedDatetime = productData["category"]["parent"]["updatedDatetime"]
        product.category_parent_txtUid = productData["category"]["parent"]["txtUid"]
        product.category_parent_HasProduct = productData["category"]["parent"]["HasProduct"]

        product.category_txtUid = productData["category"]["txtUid"]
        product.category_HasProduct = productData["category"]["HasProduct"]

        product.productimages = productData["productimages"]

        product.productextension_id = productData["productextension"]["id"]
        product.productextension_minimumOrderQuantity = productData["productextension"]["minimumOrderQuantity"]
        product.productextension_minimumDisplayQuantity = productData["productextension"]["minimumDisplayQuantity"]
        product.productextension_goodSalesQuantity = productData["productextension"]["goodSalesQuantity"]
        product.productextension_normalSalesQuantity = productData["productextension"]["normalSalesQuantity"]
        product.productextension_optimalStockQuantity = productData["productextension"]["optimalStockQuantity"]
        product.productextension_isLocked = productData["productextension"]["isLocked"]

        product.supplier_txtUid = productData["supplier"]["txtUid"]
        product.supplier_id = productData["supplier"]["id"]
        product.supplier_uid = productData["supplier"]["uid"]
        product.supplier_name = productData["supplier"]["name"]
        product.supplier_linkman = productData["supplier"]["linkman"]
        product.supplier_gender = productData["supplier"]["gender"]
        product.supplier_tel = productData["supplier"]["tel"]
        product.supplier_email = productData["supplier"]["email"]
        product.supplier_address = productData["supplier"]["address"]
        product.supplier_remarks = productData["supplier"]["remarks"]
        product.supplier_enable = productData["supplier"]["enable"]
        
        if "createdDatetime" in productData["supplier"]:
            product.supplier_createdDatetime = productData["supplier"]["createdDatetime"]
            product.supplier_updatedDatetime = productData["supplier"]["updatedDatetime"]

        product.categoryShowId = productData["categoryShowId"]
        product.parentHas = productData["parentHas"]
        product.txtUid = productData["txtUid"]
        product.updateStock = productData["updateStock"]
        product.isOutOfStock = productData["isOutOfStock"]

        product.productUnitExchangeList = []

        for exchangeList in productData["productUnitExchangeList"]:
            oneEchangeList = self.parseExchangeList(exchangeList)
            product.productUnitExchangeList.append(oneEchangeList)

        product.isCurrentPrice = productData["isCurrentPrice"]
        product.disableEntireDiscount = productData["disableEntireDiscount"]
        product.isPrior = productData["isPrior"]
        product.enableBatch = productData["enableBatch"]
        product.hideFromClient = productData["hideFromClient"]

        product.specNum = productData["specNum"]
        product.isEnableVirtualStock = productData["isEnableVirtualStock"]
        product.ignoreStock = productData["ignoreStock"]
        product.dataIndex = productData["dataIndex"]
        product.sellPriceIsNull = productData["sellPriceIsNull"]

        product.spu = productData["spu"]
        product.id = productData["id"]
        product.uid = productData["uid"]
        product.categoryUid = productData["categoryUid"]
        product.supplierUid = productData["supplierUid"]

        product.userId = productData["userId"]
        product.name = productData["name"]
        product.barcode = productData["barcode"]
        product.buyPrice = productData["buyPrice"]
        product.sellPrice = productData["sellPrice"]

        product.stock = productData["stock"]
        if ("maxStock" in productData):
            product.maxStock = productData["maxStock"]
        if ("minStock" in productData):
            product.minStock = productData["minStock"]
        product.pinyin = productData["pinyin"]
        product.sellPrice2 = productData["sellPrice2"]

        product.customerPrice = productData["customerPrice"]
        product.productionDate = productData["productionDate"]
        product.attribute1 = productData["attribute1"]
        product.attribute2 = productData["attribute2"]
        product.attribute3 = productData["attribute3"]

        product.attribute4 = productData["attribute4"]
        product.isPoint = productData["isPoint"]
        product.isCustomerDiscount = productData["isCustomerDiscount"]
        product.enable = productData["enable"]
        product.description = productData["description"]

        product.createdDatetime = productData["createdDatetime"]
        product.updatedDatetime = productData["updatedDatetime"]
        product.isGift = productData["isGift"]
        product.isCaseProduct = productData["isCaseProduct"]
        product.attribute5 = productData["attribute5"]

        product.attribute6 = productData["attribute6"]
        product.attribute7 = productData["attribute7"]
        product.attribute8 = productData["attribute8"]
        product.attribute9 = productData["attribute9"]
        product.attribute10 = productData["attribute10"]
        
        return product

