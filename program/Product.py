
class Product(object):
    def __init__(self):
        self.category_id = 0
        self.category_uid = 0
        self.category_name = ""
        self.category_enable = 0
        self.category_createdDatetime = ""
        self.category_updatedDatetime = ""
        self.category_parent_id = 0
        self.category_parent_uid = 0
        self.category_parent_name = ""
        self.category_parent_enable = 0
        self.category_parent_createdDatetime = ""
        self.category_parent_updatedDatetime = ""
        self.category_parent_txtUid = ""
        self.category_parent_HasProduct = False
        self.category_txtUid = ""
        self.category_HasProduct = False

        self.productimages = []

        self.productextension_id = 0
        self.productextension_minimumOrderQuantity = 0.0
        self.productextension_minimumDisplayQuantity = 0.0
        self.productextension_goodSalesQuantity = 0.0
        self.productextension_normalSalesQuantity = 0.0
        self.productextension_optimalStockQuantity = 0.0
        self.productextension_isLocked = False

        self.supplier_txtUid = ""
        self.supplier_id = 0
        self.supplier_uid = 0
        self.supplier_name = ""
        self.supplier_linkman = ""
        self.supplier_gender = ""
        self.supplier_tel = ""
        self.supplier_email = ""
        self.supplier_address = ""
        self.supplier_remarks = ""
        self.supplier_enable = 1
        self.supplier_createdDatetime = ""
        self.supplier_updatedDatetime = ""

        self.categoryShowId = 0
        self.parentHas = 0
        self.txtUid = ""
        self.updateStock = 0
        self.isOutOfStock = True

        ## this one needs another object
        self.productUnitExchangeList = []

        self.isCurrentPrice = False
        self.disableEntireDiscount = False
        self.isPrior = False
        self.enableBatch = 0
        self.hideFromClient = 0
        self.specNum = 0
        self.isEnableVirtualStock = False
        self.ignoreStock = False
        self.dataIndex = 0
        self.sellPriceIsNull = False
        self.spu = ""
        self.id = 0
        self.uid = 0
        self.categoryUid = 0
        self.supplierUid = 0
        self.userId = 0
        self.name = ""
        self.barcode = ""
        self.buyPrice = 0.0
        self.sellPrice = 0.0
        self.stock = 0.0
        self.maxStock = 0.0
        self.minStock = 0.0
        self.pinyin = ""
        self.sellPrice2 = 0.0
        self.customerPrice = 0.0
        self.productionDate = ""
        self.attribute1 = ""
        self.attribute2 = ""
        self.attribute3 = ""
        self.attribute4 = ""
        self.isPoint = 0
        self.isCustomerDiscount = 0
        self.enable = 0
        self.description = ""
        self.createdDatetime = ""
        self.updatedDatetime = ""
        self.isGift = 0
        self.isCaseProduct = 0
        self.attribute5 = ""
        self.attribute6 = ""
        self.attribute7 = ""
        self.attribute8 = ""
        self.attribute9 = ""
        self.attribute10 = ""
       

class ProductUnitExchangeList(object):
    def __init__(self):
        productUnitName = ""
        productUnitTxtUid = ""
        id = 0,
        userId = 0,
        productUid = 0,
        productUnitUid = 0,
        exchangeQuantity = 0.0,
        isBase = 0,
        enable = 0,
        isRequest = 0,
        unitQuantity = 0.0,
        baseUnitQuantity = 0.0