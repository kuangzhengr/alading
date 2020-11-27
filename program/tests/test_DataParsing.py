import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

import unittest
import DataParsing
import Product
import os
import json

class testDataParsing(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        script_dir += "\productData_test" 
        rel_path = "productData.json"
        abs_file_path = os.path.join(script_dir, rel_path)

        with open(abs_file_path, 'rb') as f:
            self.productData = json.load(f)
        self.dataParsing = DataParsing.DataParsing()
        self.product = Product.Product()

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parseCategory(self):
        self.dataParsing.parseCategory(self.product, self.productData)
        self.assertEqual(getattr(self.product, "category_id"), 1)
        self.assertEqual(getattr(self.product, "category_uid"), 1538011898303974682)
        self.assertEqual(getattr(self.product, "category_name"), "熟食")
        self.assertEqual(getattr(self.product, "category_enable"), 1)
        self.assertEqual(getattr(self.product, "category_createdDatetime"), "2018-09-27 09:31:38")
        self.assertEqual(getattr(self.product, "category_updatedDatetime"), "2018-09-27 09:31:50")
        self.assertEqual(getattr(self.product, "category_parent_id"), 123)
        self.assertEqual(getattr(self.product, "category_parent_uid"), 456)
        self.assertEqual(getattr(self.product, "category_parent_name"), "asdf")
        self.assertEqual(getattr(self.product, "category_parent_enable"), 6)
        self.assertEqual(getattr(self.product, "category_parent_createdDatetime"), "2020-04-20 05:51:34")
        self.assertEqual(getattr(self.product, "category_parent_updatedDatetime"), "2020-04-20 05:51:37")
        self.assertEqual(getattr(self.product, "category_parent_txtUid"), "99")
        self.assertEqual(getattr(self.product, "category_parent_HasProduct"), False)
        self.assertEqual(getattr(self.product, "category_txtUid"), "1538011898303974682")
        self.assertEqual(getattr(self.product, "category_HasProduct"), True)

    def test_parseProductExtension(self):
        self.dataParsing.parseProductExtension(self.product, self.productData)
        self.assertEqual(getattr(self.product, "productextension_id"), 789)
        self.assertEqual(getattr(self.product, "productextension_minimumOrderQuantity"), 10.0)
        self.assertEqual(getattr(self.product, "productextension_minimumDisplayQuantity"), 11.0)
        self.assertEqual(getattr(self.product, "productextension_goodSalesQuantity"), 12.0)
        self.assertEqual(getattr(self.product, "productextension_normalSalesQuantity"), 13.0)
        self.assertEqual(getattr(self.product, "productextension_optimalStockQuantity"), 14.0)
        self.assertEqual(getattr(self.product, "productextension_isLocked"), False)

    def test_parseSupplier(self):
        self.dataParsing.parseSupplier(self.product, self.productData)
        self.assertEqual(getattr(self.product, "supplier_txtUid"),"1107322288086534946")
        self.assertEqual(getattr(self.product, "supplier_id"), 654)
        self.assertEqual(getattr(self.product, "supplier_uid"), 1107322288086534946)
        self.assertEqual(getattr(self.product, "supplier_name"), "阿拉叮(件出Z)")
        self.assertEqual(getattr(self.product, "supplier_linkman"), "abc")
        self.assertEqual(getattr(self.product, "supplier_gender"), "男")
        self.assertEqual(getattr(self.product, "supplier_tel"), "112233")
        self.assertEqual(getattr(self.product, "supplier_email"), "qqq")
        self.assertEqual(getattr(self.product, "supplier_address"), "www")
        self.assertEqual(getattr(self.product, "supplier_remarks"), "eee")
        self.assertEqual(getattr(self.product, "supplier_enable"), 1)
        self.assertEqual(getattr(self.product, "supplier_createdDatetime"), "2019-11-13 16:46:30")
        self.assertEqual(getattr(self.product, "supplier_updatedDatetime"), "2019-11-13 16:46:40")

    def test_parseGeneral(self):
        self.dataParsing.parseGeneral(self.product, self.productData)
        self.assertEqual(getattr(self.product, "productimages"), [])

        self.assertEqual(getattr(self.product, "categoryShowId"), 98)
        self.assertEqual(getattr(self.product, "parentHas"), 125)
        self.assertEqual(getattr(self.product, "txtUid"), "933491598723914016")
        self.assertEqual(getattr(self.product, "updateStock"), 65.0)
        self.assertEqual(getattr(self.product, "isOutOfStock"), False)

        self.assertEqual(getattr(self.product, "isCurrentPrice"), False)
        self.assertEqual(getattr(self.product, "disableEntireDiscount"), True)
        self.assertEqual(getattr(self.product, "isPrior"), False)
        self.assertEqual(getattr(self.product, "enableBatch"), 9)
        self.assertEqual(getattr(self.product, "hideFromClient"), 8)

        self.assertEqual(getattr(self.product, "specNum"), 7)
        self.assertEqual(getattr(self.product, "isEnableVirtualStock"), False)
        self.assertEqual(getattr(self.product, "ignoreStock"), True)
        self.assertEqual(getattr(self.product, "dataIndex"), 6)
        self.assertEqual(getattr(self.product, "sellPriceIsNull"), False)

        self.assertEqual(getattr(self.product, "spu"), "0010002")
        self.assertEqual(getattr(self.product, "id"), 63063433)
        self.assertEqual(getattr(self.product, "uid"), 933491598723914016)
        self.assertEqual(getattr(self.product, "categoryUid"), 1538011898303974682)
        self.assertEqual(getattr(self.product, "supplierUid"), 1107322288086534946)

        self.assertEqual(getattr(self.product, "userId"), 3834525)
        self.assertEqual(getattr(self.product, "name"), "四海咖喱/")
        self.assertEqual(getattr(self.product, "barcode"), "0010002")
        self.assertEqual(getattr(self.product, "buyPrice"), 9.0)
        self.assertEqual(getattr(self.product, "sellPrice"), 10.0)

        self.assertEqual(getattr(self.product, "stock"), 5.0)
        self.assertEqual(getattr(self.product, "maxStock"), 5.0)
        self.assertEqual(getattr(self.product, "minStock"), 3.0)
        self.assertEqual(getattr(self.product, "pinyin"), "szkl")
        self.assertEqual(getattr(self.product, "sellPrice2"), 9.0)

        self.assertEqual(getattr(self.product, "customerPrice"), 15.0)
        self.assertEqual(getattr(self.product, "productionDate"), "147")
        self.assertEqual(getattr(self.product, "attribute1"), "258")
        self.assertEqual(getattr(self.product, "attribute2"), "369")
        self.assertEqual(getattr(self.product, "attribute3"), "753")

        self.assertEqual(getattr(self.product, "attribute4"), "951")
        self.assertEqual(getattr(self.product, "isPoint"), 1)
        self.assertEqual(getattr(self.product, "isCustomerDiscount"), 1.2)
        self.assertEqual(getattr(self.product, "enable"), 1)
        self.assertEqual(getattr(self.product, "description"), "zzz")

        self.assertEqual(getattr(self.product, "createdDatetime"), "2019-11-18 21:55:31")
        self.assertEqual(getattr(self.product, "updatedDatetime"), "2020-03-14 15:44:35")
        self.assertEqual(getattr(self.product, "isGift"), 0)
        self.assertEqual(getattr(self.product, "isCaseProduct"), 23)
        self.assertEqual(getattr(self.product, "attribute5"), "c")

        self.assertEqual(getattr(self.product, "attribute6"), "d")
        self.assertEqual(getattr(self.product, "attribute7"), "e")
        self.assertEqual(getattr(self.product, "attribute8"), "f")
        self.assertEqual(getattr(self.product, "attribute9"), "g")
        self.assertEqual(getattr(self.product, "attribute10"), "a")

    def test_parseproductUnitExchangeList(self):
        self.dataParsing.parseproductUnitExchangeList(self.product, self.productData)
        self.assertEqual(len(self.product.productUnitExchangeList), 1)

        self.assertEqual(getattr(self.product.productUnitExchangeList[0], "productUnitName"), "包")
        self.assertEqual(getattr(self.product.productUnitExchangeList[0], "productUnitTxtUid"), "1573110659316662375")
        self.assertEqual(getattr(self.product.productUnitExchangeList[0], "id"), 27049001)
        self.assertEqual(getattr(self.product.productUnitExchangeList[0], "userId"), 3834525)
        self.assertEqual(getattr(self.product.productUnitExchangeList[0], "productUid"), 933491598723914016)
        self.assertEqual(getattr(self.product.productUnitExchangeList[0], "productUnitUid"), 1573110659316662375)
        self.assertEqual(getattr(self.product.productUnitExchangeList[0], "exchangeQuantity"), 1.0)
        self.assertEqual(getattr(self.product.productUnitExchangeList[0], "isBase"), 1)
        self.assertEqual(getattr(self.product.productUnitExchangeList[0], "enable"), 2)
        self.assertEqual(getattr(self.product.productUnitExchangeList[0], "isRequest"), 0)
        self.assertEqual(getattr(self.product.productUnitExchangeList[0], "unitQuantity"), 5)
        self.assertEqual(getattr(self.product.productUnitExchangeList[0], "baseUnitQuantity"), 8)



if __name__ == '__main__':
    unittest.main()
         