import json
import os
import Product
import DataParsing

class DataChecking(object):
    def __init__(self, store_records):
        """
        constructor initialize fields to store:
            product info
            policy query
            violation messages
            function table for different check
            error message function table for adding different violation message
        """
        self.store_records = store_records
        self.query = None
        self.violation = {}
        self.functions = {
            "GT" : self.greater,
            "LT" : self.less,
            "EQ" : self.equal,
            "BOOL" : self.bool,
            "FORMAT" : self.format,
            "NULL" : self.null,
            "EXIST" : self.exist,
            "IS" : self.isComare,
            "IF" : self.ifstatement,
        }
        self.errorMsgFunc = {
            "GT" : self.greaterMsg,
            "LT" : self.lessMsg,
            "EQ" : self.equalMsg,
            "BOOL" : self.boolMsg,
            "FORMAT" : self.formatMsg,
            "NULL" : self.nullMsg,
            "EXIST" : self.existMsg,
            "IF" : self.ifstatementMsg,
            "IS" : self.isComareMsg,
        }
        self.mathFuctions = {
            "ADD" : self.add,
            "SUB" : self.sub,
            "MUL" : self.mul,
            "DIV" : self.div,
        }
        print("Number of store record: " + str(len(self.store_records)))
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        script_dir += "\query_interval" 
        rel_path = "query.json"
        abs_file_path = os.path.join(script_dir, rel_path)

        with open(abs_file_path, 'rb') as f:
            self.query = json.load(f)


    def checkData(self):
        """
        loop over the whole product records in each store(json file)
        apply every policy onto each product to check if there is violation

        Will store the violation information into the violation field 
        """
        policyBody_list = []
        function_list = []
        errorMsgFunction_list = []

        for aPolicy in self.query:
            self.processOnePolicy(aPolicy, policyBody_list, function_list, errorMsgFunction_list)

        for store_key in self.store_records:
            self.violation[store_key] = []
            for product in self.store_records[store_key]:
                for i in range(len(policyBody_list)):
                    if not function_list[i](policyBody_list[i], product, store_key):
                        errorMsgFunction_list[i](policyBody_list[i], product, store_key)

        print("Total Violation: " + str(len(self.violation["store_1.json"])))


    def processOnePolicy(self, aPolicy, policyBody_list, function_list, errorMsgFunction_list):
        """
        process one policy from the policy query
        store the policy function and corespondent policy body to put in the function
        store the error message generate function to the list
        """
        for key in aPolicy:
            print(aPolicy[key])
            func = self.functions.get(key, self.invalidKey)
            function_list.append(func)
            policyBody_list.append(aPolicy[key])
            errorMsgFunc = self.errorMsgFunc.get(key, self.invalidKey)
            errorMsgFunction_list.append(errorMsgFunc)


    def mathComparison(self, compareFunc, policy, product, store_key):
        """
        check the products with compare function function to see
        if the policy body key is comply with the compare function to compare value

        Will store the violation information into the violation field
        return true if product did not violate the policy, and false if it did violate
        """
        for key in policy: # example key = "sellPrice"
            if isinstance(policy[key], str):
                if not compareFunc(getattr(product, key), getattr(product, policy[key])): # example sellPrice < buyPrice
                    return False
            elif isinstance(policy[key], list):
                func = self.mathFuctions.get(policy[key][1], self.invalidMathKey)
                compare_value = func(product, policy[key][0], policy[key][2])
                if not compareFunc(getattr(product, key), compare_value): # example sellPrice < buyPrice + 10
                    return False
            else:
                if not compareFunc(getattr(product, key), policy[key]): # example sellPrice < 100
                    return False
            return True

    def greater(self, policy, product, store_key):
        """
        check the products with this function to see
        if the policy body key is greater than the compare value

        Will store the violation information into the violation field
        return true if product did not violate the policy, and false if it did violate
        """
        return self.mathComparison(self.greaterThan, policy, product, store_key)
    
    def less(self, policy, product, store_key):
        """
        check the products with this function to see
        if the policy body key is less than the compare value

        Will store the violation information into the violation field 
        return true if product did not violate the policy, and false if it did violate
        """
        return self.mathComparison(self.lessThan, policy, product, store_key)

    def equal(self, policy, product, store_key):
        """
        check the products with this function to see
        if the policy body key is equal to the compare value

        Will store the violation information into the violation field 
        return true if product did not violate the policy, and false if it did violate
        """
        return self.mathComparison(self.equalTo, policy, product, store_key)


    def bool(self, policy, product, store_key):
        """
        check the products with this function to see
        if the policy body key is set equal to the compare value

        Will store the violation information into the violation field 
        return true if product did not violate the policy, and false if it did violate
        """
        for key in policy: # example key = "category_parent_HasProduct"
            if getattr(product, key) != policy[key]:
                return False
            return True


    def format(self, policy, product, store_key):
        """
        check the products with this function to see
        if the policy body key is set to the require format

        Will store the violation information into the violation field 
        return true if product did not violate the policy, and false if it did violate
        """
        for key in policy: # example key = "supplier_createdDatetime"
            format = policy[key]
            productInput = getattr(product, key)
            if (len(format) != len(productInput)):
                return False

            #loop over check instance of
            for i in range(len(format)): # ex. "0000-00-00 00:00:00"
                if (format[i].isdigit()):
                    if (not productInput[i].isdigit()):
                        return False
                elif (format[i].isalpha()):
                    if (not productInput[i].isalpha()):
                        return False
                else: # '-' ':' or other symbolic chars
                    if (productInput[i] != format[i]):
                        return False
            return True

    def exist(self, policy, product, store_key):
        """
        check the products with this function to see
        if the policy body key is exist/not exist in another store (an expensive check)

        return true or false for the if statement
        """
        for key in policy: # example key = "store_2"
            other_store_key = key + ".json" 
            shouldExist = policy[key] # true or false
            existFlag = False
            for other_store_product in self.store_records[other_store_key]:
                other_id = getattr(other_store_product, "id")
                id = getattr(product, "id")
                if (other_id == id):
                    existFlag = True
            
            if (existFlag == shouldExist):
                return True
            else:
                return False


    def null(self, policy, product, store_key):
        """
        check the products with this function to see
        if the policy body key is null/not null
        here either [], "" would be consider as null which is no enter

        Will store the violation information into the violation field 
        return true if product did not violate the policy, and false if it did violate
        """
        for key in policy: # example key = "productimages"
            should_be_null = policy[key] # true or false
            productAttr = getattr(product, key)
            if (should_be_null):
                if (productAttr != [] and productAttr != ""):
                    return False
            else:
                if (productAttr == [] or productAttr == ""):
                    return False
            return True

    def isComare(self, policy, product, store_key):
        """
        check the products with this function to see
        if the product attribute has the same string as in policy body 

        Will store the violation information into the violation field 
        return true if product did not violate the policy, and false if it did violate
        """
        key, val = list(policy.items())[0]  # key = "attribute5" , val = ""
        productAttr = getattr(product, key)

        if (productAttr != val):
            return False

        return True

    def ifstatement(self, policy, product, store_key):
        """
        condition check
        if the product fulfill the condition in the if clause
        then check the condition from the requirement block

        Will store the violation information into the violation field 
        """
        condition = policy[0]      #"IS": {"supplierUID" : 12345}
        requirement = policy[1]    #"EXIST": {"store_2" : true}

        condition_comparator, condition_body = list(condition.items())[0]
        require_comparator, require_body = list(requirement.items())[0]

        condition_function = self.functions.get(condition_comparator, self.invalidKey)
        require_function = self.functions.get(require_comparator, self.invalidKey)

        if condition_function(condition_body, product, store_key):  # condition fulfilled
            if not require_function(require_body, product, store_key): # requirement violated
                return False

        return True
        
    ## simple helper function ---------------------------------------
    def greaterThan(self, left, right):
        return left > right

    def equalTo(self, left, right):
        return left == right

    def lessThan(self, left, right):
        return left < right
  
    def add(self, product, productKey, value):
        """
        return sum of product key and value
        """
        return getattr(product, productKey) + value

    def sub(self, product, productKey, value):
        """
        return subtratction of product key and value
        """
        return getattr(product, productKey) - value

    def mul(self, product, productKey, value):
        """
        return multiplication of product key and value
        """
        return round(getattr(product, productKey) * value, 2)

    def div(self, product, productKey, value):
        """
        return divition of product key and value
        """
        return round((getattr(product, productKey) / value), 2)

    ## Message generation part ---------------------------------------
    def greaterMsg(self, policyBody, product, store_key):
        base_msg = " is not greater than: "
        self.addBasicMsg(base_msg, policyBody, product, store_key)

    def lessMsg(self, policyBody, product, store_key):
        base_msg = " is not less than: "
        self.addBasicMsg(base_msg, policyBody, product, store_key)

    def equalMsg(self, policyBody, product, store_key):
        base_msg = " is not equal to: "
        self.addBasicMsg(base_msg, policyBody, product, store_key)

    def boolMsg(self, policyBody, product, store_key):
        base_msg = " is not set to: "
        self.addBasicMsg(base_msg, policyBody, product, store_key)

    def formatMsg(self, policyBody, product, store_key):
        base_msg = " is not following the format: "
        self.addBasicMsg(base_msg, policyBody, product, store_key)

    def existMsg(self, policyBody, product, store_key):
        base_msg = " is violating the existence requirement of: "
        self.addBasicMsg(base_msg, policyBody, product, store_key)

    def nullMsg(self, policyBody, product, store_key):
        violation_msg = ""
        key, should_be_null = list(policyBody.items())[0]
        if (should_be_null):
            violation_msg = key + " enter should be null." + " Product ID: " + str(product.id)
        else:
            violation_msg = key + " enter should not be null." + " Product ID: " + str(product.id)
        
        self.violation[store_key].append(violation_msg)

    def isComareMsg(self, policyBody, product, store_key):
        base_msg = " is not set to: "
        self.addBasicMsg(base_msg, policyBody, product, store_key)

    def ifstatementMsg(self, policyBody, product, store_key):
        condition = policyBody[0]      #"IS": {"supplierUID" : 12345}
        requirement = policyBody[1]    #"EXIST": {"store_2" : true}

        condition_comparator, condition_body = list(condition.items())[0]
        condBody_key, condBody_val = list(condition_body.items())[0]
        require_comparator, require_body = list(requirement.items())[0]

        self.errorMsgFunc[require_comparator](require_body, product, store_key)
        append_Msg = " <due to if statemnt: " + condBody_key + " " + condition_comparator + " " + str(condBody_val) + ">"
        (self.violation[store_key])[-1] += append_Msg

    def addBasicMsg(self, base_msg, policyBody, product, store_key):
        key, value = list(policyBody.items())[0]
        whole_msg = self.getBasicMsg(base_msg, key, value, product)
        self.violation[store_key].append(whole_msg)

    def getBasicMsg(self, msg, leftKey, rightKey, product):
        if rightKey == "":
            rightKey = "Empty String"
        return leftKey + msg + str(rightKey) + " Product ID: " + str(product.id)


    # Default functions -------------------------------------------------
    def invalidKey(self, policy, product, store_key):
        """
        invalidKey handler
        It is possible to add invalidKey excpetion feature
        Whenever an invalid key in the query is detected, the program halt and a 
        notification message will send to sys operator 

        For now I just skip it
        """
        None
        #print("invalid key")

    def invalidMathKey(self, product, productKey, value):
        """
        invalidKey handler
        It is possible to add invalidKey excpetion feature
        Whenever an invalid key in the query is detected, the program halt and a 
        notification message will send to sys operator 

        For now just skip it
        """
        None
        #print("invalid math key")

