import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

import unittest
import DataChecking
import DataParsing
import Product
import os
import json

class testDataChecking(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        script_dir += "./query_test" 
        product_path = "productData.json"
        product_file_path = os.path.join(script_dir, product_path)

        gt_path = "GT.json"
        gt_file_path = os.path.join(script_dir, gt_path)

        lt_path = "LT.json"
        lt_file_path = os.path.join(script_dir, lt_path)

        eq_path = "EQ.json"
        eq_file_path = os.path.join(script_dir, eq_path)

        bool_path = "BOOL.json"
        bool_file_path = os.path.join(script_dir, bool_path)

        format_path = "FORMAT.json"
        format_file_path = os.path.join(script_dir, format_path)

        null_path = "NULL.json"
        null_file_path = os.path.join(script_dir, null_path)

        exist_path = "EXIST.json"
        exist_file_path = os.path.join(script_dir, exist_path)

        if_path = "IF.json"
        if_file_path = os.path.join(script_dir, if_path)

        is_path = "IS.json"
        is_file_path = os.path.join(script_dir, is_path)

        with open(product_file_path, 'rb') as f:
            productData = json.load(f)

        with open(gt_file_path, 'rb') as f:
            self.gt_query = json.load(f)

        with open(lt_file_path, 'rb') as f:
            self.lt_query = json.load(f)

        with open(eq_file_path, 'rb') as f:
            self.eq_query = json.load(f)

        with open(bool_file_path, 'rb') as f:
            self.bool_query = json.load(f)

        with open(format_file_path, 'rb') as f:
            self.format_query = json.load(f)

        with open(null_file_path, 'rb') as f:
            self.null_query = json.load(f)

        with open(exist_file_path, 'rb') as f:
            self.exist_query = json.load(f)

        with open(if_file_path, 'rb') as f:
            self.if_query = json.load(f)

        with open(is_file_path, 'rb') as f:
            self.is_query = json.load(f)
        
        self.dataParsing = DataParsing.DataParsing()
        self.product = self.dataParsing.parseData(productData)
        self.dataChecking = DataChecking.DataChecking([])

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_processOnePolicy(self):
        policyBody_list = []
        function_list = []
        errorMsgFunction_list = []

        self.dataChecking.processOnePolicy(self.gt_query, policyBody_list, function_list, errorMsgFunction_list)
        self.assertEqual(policyBody_list[0], {"sellPrice" : "buyPrice" })
        self.assertEqual(function_list[0], self.dataChecking.functions["GT"])
        self.assertEqual(errorMsgFunction_list[0], self.dataChecking.errorMsgFunc["GT"])

        self.dataChecking.processOnePolicy(self.lt_query, policyBody_list, function_list, errorMsgFunction_list)
        self.assertEqual(policyBody_list[1], {"sellPrice" : ["buyPrice", "DIV", 1.05]})
        self.assertEqual(function_list[1], self.dataChecking.functions["LT"])
        self.assertEqual(errorMsgFunction_list[1], self.dataChecking.errorMsgFunc["LT"])

        self.dataChecking.processOnePolicy(self.eq_query, policyBody_list, function_list, errorMsgFunction_list)
        self.assertEqual(policyBody_list[2], {"spu" : "barcode"})
        self.assertEqual(function_list[2], self.dataChecking.functions["EQ"])
        self.assertEqual(errorMsgFunction_list[2], self.dataChecking.errorMsgFunc["EQ"])

        self.dataChecking.processOnePolicy(self.bool_query, policyBody_list, function_list, errorMsgFunction_list)
        self.assertEqual(policyBody_list[3], {"category_name" : False})
        self.assertEqual(function_list[3], self.dataChecking.functions["BOOL"])
        self.assertEqual(errorMsgFunction_list[3], self.dataChecking.errorMsgFunc["BOOL"])

        self.dataChecking.processOnePolicy(self.format_query, policyBody_list, function_list, errorMsgFunction_list)
        self.assertEqual(policyBody_list[4], {"category_createdDatetime" : "0000-00-00 00:00:00"})
        self.assertEqual(function_list[4], self.dataChecking.functions["FORMAT"])
        self.assertEqual(errorMsgFunction_list[4], self.dataChecking.errorMsgFunc["FORMAT"])

        self.dataChecking.processOnePolicy(self.null_query, policyBody_list, function_list, errorMsgFunction_list)
        self.assertEqual(policyBody_list[5], {"category_name" : False})
        self.assertEqual(function_list[5], self.dataChecking.functions["NULL"])
        self.assertEqual(errorMsgFunction_list[5], self.dataChecking.errorMsgFunc["NULL"])

        self.dataChecking.processOnePolicy(self.exist_query, policyBody_list, function_list, errorMsgFunction_list)
        self.assertEqual(policyBody_list[6], {"test_store" : True })
        self.assertEqual(function_list[6], self.dataChecking.functions["EXIST"])
        self.assertEqual(errorMsgFunction_list[6], self.dataChecking.errorMsgFunc["EXIST"])
        
        self.dataChecking.processOnePolicy(self.if_query, policyBody_list, function_list, errorMsgFunction_list)
        self.assertEqual(policyBody_list[7], [{"EQ": {"sellPrice" : 100}}, {"GT" : {"buyPrice" : 80}}])
        self.assertEqual(function_list[7], self.dataChecking.functions["IF"])
        self.assertEqual(errorMsgFunction_list[7], self.dataChecking.errorMsgFunc["IF"])

        self.dataChecking.processOnePolicy(self.is_query, policyBody_list, function_list, errorMsgFunction_list)
        self.assertEqual(policyBody_list[8], {"category_parent_name" : ""})
        self.assertEqual(function_list[8], self.dataChecking.functions["IS"])
        self.assertEqual(errorMsgFunction_list[8], self.dataChecking.errorMsgFunc["IS"])


    def test_gtFunc(self):
        self.assertEqual(getattr(self.product, "buyPrice"), 100)
        self.assertEqual(getattr(self.product, "sellPrice"), 110)

        numberBody_greater = {"buyPrice": 200}
        numberBody_greater_edge = {"buyPrice": 101}
        numberBody_equal = {"buyPrice": 100}
        numberBody_smaller_edge = {"buyPrice": 99}
        numberBody_smaller = {"buyPrice": 10}
        self.assertFalse(self.dataChecking.greater(numberBody_greater, self.product, "test"))
        self.assertFalse(self.dataChecking.greater(numberBody_greater_edge, self.product, "test"))
        self.assertFalse(self.dataChecking.greater(numberBody_equal, self.product, "test"))
        self.assertTrue(self.dataChecking.greater(numberBody_smaller_edge, self.product, "test"))
        self.assertTrue(self.dataChecking.greater(numberBody_smaller, self.product, "test"))

        arrayBody_greater = {"buyPrice": ["sellPrice", "ADD", 10]}
        arrayBody_greater_edge = {"buyPrice": ["sellPrice", "SUB", 9]}
        arrayBody_equal = {"buyPrice": ["sellPrice", "SUB", 10]}
        arrayBody_smaller_edge = {"buyPrice": ["sellPrice", "MUL", 0.9]}
        arrayBody_smaller = {"buyPrice": ["sellPrice", "DIV", 2]}
        self.assertFalse(self.dataChecking.greater(arrayBody_greater, self.product, "test"))
        self.assertFalse(self.dataChecking.greater(arrayBody_greater_edge, self.product, "test"))
        self.assertFalse(self.dataChecking.greater(arrayBody_equal, self.product, "test"))
        self.assertTrue(self.dataChecking.greater(arrayBody_smaller_edge, self.product, "test"))
        self.assertTrue(self.dataChecking.greater(arrayBody_smaller, self.product, "test"))

        stringBody_less = {"buyPrice": "sellPrice"}
        stringBody_greater = {"sellPrice": "buyPrice"}
        stringBody_eq = {"buyPrice": "sellPrice2"}
        self.assertFalse(self.dataChecking.greater(stringBody_less, self.product, "test"))
        self.assertTrue(self.dataChecking.greater(stringBody_greater, self.product, "test"))
        self.assertFalse(self.dataChecking.greater(stringBody_eq, self.product, "test"))


    def test_ltFunc(self):
        self.assertEqual(getattr(self.product, "buyPrice"), 100)
        self.assertEqual(getattr(self.product, "sellPrice"), 110)

        numberBody_greater = {"buyPrice": 200}
        numberBody_greater_edge = {"buyPrice": 101}
        numberBody_equal = {"buyPrice": 100}
        numberBody_smaller_edge = {"buyPrice": 99}
        numberBody_smaller = {"buyPrice": 10}
        self.assertTrue(self.dataChecking.less(numberBody_greater, self.product, "test"))
        self.assertTrue(self.dataChecking.less(numberBody_greater_edge, self.product, "test"))
        self.assertFalse(self.dataChecking.less(numberBody_equal, self.product, "test"))
        self.assertFalse(self.dataChecking.less(numberBody_smaller_edge, self.product, "test"))
        self.assertFalse(self.dataChecking.less(numberBody_smaller, self.product, "test"))

        stringBody_less = {"buyPrice": "sellPrice"}
        stringBody_greater = {"sellPrice": "buyPrice"}
        stringBody_eq = {"buyPrice": "sellPrice2"}
        self.assertTrue(self.dataChecking.less(stringBody_less, self.product, "test"))
        self.assertFalse(self.dataChecking.less(stringBody_greater, self.product, "test"))
        self.assertFalse(self.dataChecking.less(stringBody_eq, self.product, "test"))

    def test_eqFunc(self):
        self.assertEqual(getattr(self.product, "buyPrice"), 100)
        self.assertEqual(getattr(self.product, "sellPrice"), 110)
        self.assertEqual(getattr(self.product, "sellPrice2"), 100)

        numberBody_greater = {"buyPrice": 200}
        numberBody_greater_edge = {"buyPrice": 101}
        numberBody_equal = {"buyPrice": 100}
        numberBody_smaller_edge = {"buyPrice": 99}
        numberBody_smaller = {"buyPrice": 10}
        self.assertFalse(self.dataChecking.equal(numberBody_greater, self.product, "test"))
        self.assertFalse(self.dataChecking.equal(numberBody_greater_edge, self.product, "test"))
        self.assertTrue(self.dataChecking.equal(numberBody_equal, self.product, "test"))
        self.assertFalse(self.dataChecking.equal(numberBody_smaller_edge, self.product, "test"))
        self.assertFalse(self.dataChecking.equal(numberBody_smaller, self.product, "test"))

        stringBody_less = {"buyPrice": "sellPrice"}
        stringBody_greater = {"sellPrice": "buyPrice"}
        stringBody_eq = {"buyPrice": "sellPrice2"}
        self.assertFalse(self.dataChecking.equal(stringBody_less, self.product, "test"))
        self.assertFalse(self.dataChecking.equal(stringBody_greater, self.product, "test"))
        self.assertTrue(self.dataChecking.equal(stringBody_eq, self.product, "test"))

    def test_boolFunc(self):
        self.assertEqual(getattr(self.product, "isCurrentPrice"), False)
        self.assertEqual(getattr(self.product, "disableEntireDiscount"), True)

        boolBody_false = {"isCurrentPrice": False}
        boolBody_true = {"isCurrentPrice": True}
        self.assertTrue(self.dataChecking.bool(boolBody_false, self.product, "test"))
        self.assertFalse(self.dataChecking.bool(boolBody_true, self.product, "test"))

        boolBody_false = {"disableEntireDiscount": False}
        boolBody_true = {"disableEntireDiscount": True}
        self.assertFalse(self.dataChecking.bool(boolBody_false, self.product, "test"))
        self.assertTrue(self.dataChecking.bool(boolBody_true, self.product, "test"))

    def test_formatFunc(self):
        self.assertEqual(getattr(self.product, "category_createdDatetime"), "2018-09-27 09:31:38")
        formatBody_origin = {"category_createdDatetime": "0000-00-00 00:00:00"}
        formatBody_monthAlpha = {"category_createdDatetime": "0000-mmm-00 00:00:00"}
        formatBody_myd = {"category_createdDatetime": "00-0000-00 00:00:00"}
        formatBody_symbol = {"category_createdDatetime": "0000/00/00 00:00:00"}
        self.assertTrue(self.dataChecking.format(formatBody_origin, self.product, "test"))
        self.assertFalse(self.dataChecking.format(formatBody_monthAlpha, self.product, "test"))
        self.assertFalse(self.dataChecking.format(formatBody_myd, self.product, "test"))
        self.assertFalse(self.dataChecking.format(formatBody_symbol, self.product, "test"))

        self.assertEqual(getattr(self.product, "category_updatedDatetime"), "2018-Sep-27 09:31:50")
        formatBody_origin = {"category_updatedDatetime": "0000-00-00 00:00:00"}
        formatBody_monthAlpha = {"category_updatedDatetime": "0000-mmm-00 00:00:00"}
        formatBody_myd = {"category_updatedDatetime": "00-0000-00 00:00:00"}
        formatBody_symbol = {"category_updatedDatetime": "0000/00/00 00:00:00"}
        self.assertFalse(self.dataChecking.format(formatBody_origin, self.product, "test"))
        self.assertTrue(self.dataChecking.format(formatBody_monthAlpha, self.product, "test"))
        self.assertFalse(self.dataChecking.format(formatBody_myd, self.product, "test"))
        self.assertFalse(self.dataChecking.format(formatBody_symbol, self.product, "test"))

        self.assertEqual(getattr(self.product, "createdDatetime"), "2019/11/18 21:55:31")
        formatBody_origin = {"createdDatetime": "0000-00-00 00:00:00"}
        formatBody_monthAlpha = {"createdDatetime": "0000-mmm-00 00:00:00"}
        formatBody_myd = {"createdDatetime": "00-0000-00 00:00:00"}
        formatBody_symbol = {"createdDatetime": "0000/00/00 00:00:00"}
        self.assertFalse(self.dataChecking.format(formatBody_origin, self.product, "test"))
        self.assertFalse(self.dataChecking.format(formatBody_monthAlpha, self.product, "test"))
        self.assertFalse(self.dataChecking.format(formatBody_myd, self.product, "test"))
        self.assertTrue(self.dataChecking.format(formatBody_symbol, self.product, "test"))

    def test_nullFunc(self):
        self.assertEqual(getattr(self.product, "attribute10"), "")
        self.assertEqual(getattr(self.product, "attribute9"), "g")

        nullBody_false = {"attribute10": False}
        nullBody_true = {"attribute10": True}
        self.assertFalse(self.dataChecking.null(nullBody_false, self.product, "test"))
        self.assertTrue(self.dataChecking.null(nullBody_true, self.product, "test"))

        nullBody_false = {"attribute9": False}
        nullBody_true = {"attribute9": True}
        self.assertTrue(self.dataChecking.null(nullBody_false, self.product, "test"))
        self.assertFalse(self.dataChecking.null(nullBody_true, self.product, "test"))

    def test_exitFunc(self):
        script_dir = os.path.dirname(__file__)
        script_dir += "./query_test" 
        product_path = "productData_notExist.json"
        product_file_path = os.path.join(script_dir, product_path)
        with open(product_file_path, 'rb') as f:
            productData_notExist = json.load(f)
            product_notExist = self.dataParsing.parseData(productData_notExist)

        product_path = "productData_exist.json"
        product_file_path = os.path.join(script_dir, product_path)
        with open(product_file_path, 'rb') as f:
            productData_exist = json.load(f)
            product_exist = self.dataParsing.parseData(productData_exist)


        store_notExist = [product_notExist]
        store_exist = [product_exist]

        self.dataChecking.store_records = {
            "store_notExist.json" : store_notExist,
            "store_exist.json" : store_exist,
        } 

        existBody_true = {"store_notExist" : True}
        existBody_false = {"store_notExist" : False}

        self.assertFalse(self.dataChecking.exist(existBody_true, self.product, "test"))
        self.assertTrue(self.dataChecking.exist(existBody_false, self.product, "test"))

        existBody_true = {"store_exist" : True}
        existBody_false = {"store_exist" : False}

        self.assertTrue(self.dataChecking.exist(existBody_true, self.product, "test"))
        self.assertFalse(self.dataChecking.exist(existBody_false, self.product, "test"))

    def test_isFunc(self):
        self.assertEqual(getattr(self.product, "name"), "四海咖喱/")
        self.assertEqual(getattr(self.product, "pinyin"), "szkl")

        isBody_false = {"name": "szkl"}
        isBody_true = {"name": "四海咖喱/"}
        self.assertFalse(self.dataChecking.isComare(isBody_false, self.product, "test"))
        self.assertTrue(self.dataChecking.isComare(isBody_true, self.product, "test"))

        isBody_true = {"pinyin": "szkl"}
        isBody_false = {"pinyin": "四海咖喱/"}
        self.assertFalse(self.dataChecking.isComare(isBody_false, self.product, "test"))
        self.assertTrue(self.dataChecking.isComare(isBody_true, self.product, "test"))

    def test_ifFunc(self):
        ifBody_TrueAndTrue = [
            {"EQ" : {"buyPrice": 100}},
            {"GT" : {"sellPrice": 100}}
        ]
        self.assertTrue(self.dataChecking.ifstatement(ifBody_TrueAndTrue, self.product, "test"))

        ## this is the only condition false will return
        ifBody_TrueAndFalse = [
            {"EQ" : {"buyPrice": 100}},
            {"LT" : {"sellPrice": 100}}
        ]
        self.assertFalse(self.dataChecking.ifstatement(ifBody_TrueAndFalse, self.product, "test"))

        ifBody_FalseAndTrue = [
            {"EQ" : {"buyPrice": 5}},
            {"GT" : {"sellPrice": 100}}
        ]
        self.assertTrue(self.dataChecking.ifstatement(ifBody_FalseAndTrue, self.product, "test"))

        ifBody_FalseAndFalse = [
            {"EQ" : {"buyPrice": 5}},
            {"LT" : {"sellPrice": 100}}
        ]
        self.assertTrue(self.dataChecking.ifstatement(ifBody_FalseAndFalse, self.product, "test"))

    def test_errorMsgGeneration(self):
        ## reset violation record
        stroe_key = "test"
        self.dataChecking.violation = {}
        self.dataChecking.violation[stroe_key] = []
        policyBody_basic = {"buyPrice": 5}
        policyBody_null_false = {"buyPrice": False}
        policyBody_null_true = {"buyPrice": True}
        policyBody_if = [
            {"EQ" : {"buyPrice": 100}},
            {"GT" : {"sellPrice": 100}}
        ]

        self.dataChecking.greaterMsg(policyBody_basic, self.product, stroe_key)
        self.assertEqual(len(self.dataChecking.violation[stroe_key]), 1)
        self.assertTrue("buyPrice is not greater than: 5" in self.dataChecking.violation[stroe_key][0])
        ## id in the msg
        self.assertTrue("63063433" in self.dataChecking.violation[stroe_key][0])

        self.dataChecking.nullMsg(policyBody_null_false, self.product, stroe_key)
        self.assertEqual(len(self.dataChecking.violation[stroe_key]), 2)
        self.assertTrue("enter should not be null." in self.dataChecking.violation[stroe_key][1])
        ## id in the msg
        self.assertTrue("63063433" in self.dataChecking.violation[stroe_key][1])

        self.dataChecking.nullMsg(policyBody_null_true, self.product, stroe_key)
        self.assertEqual(len(self.dataChecking.violation[stroe_key]), 3)
        self.assertTrue(" enter should be null." in self.dataChecking.violation[stroe_key][2])
        ## id in the msg
        self.assertTrue("63063433" in self.dataChecking.violation[stroe_key][2])

        self.dataChecking.ifstatementMsg(policyBody_if, self.product, stroe_key)
        self.assertEqual(len(self.dataChecking.violation[stroe_key]), 4)
        self.assertTrue("sellPrice is not greater than:" in self.dataChecking.violation[stroe_key][3])
        ## id in the msg
        self.assertTrue("63063433" in self.dataChecking.violation[stroe_key][3])
        ## additional info for if statment
        self.assertTrue("due to if statemnt:" in self.dataChecking.violation[stroe_key][3])





if __name__ == '__main__':
    unittest.main()
         