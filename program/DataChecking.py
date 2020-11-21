import json
import os
import Product
import DataParsing

class DataChecking(object):
    def __init__(self, store_records):
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
            "IF" : self.ifstatement, ## not implemented
            # "IS" : self.isComare.
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
        for aPolicy in self.query:
            self.processOnePolicy(aPolicy, policyBody_list, function_list)

        for store_key in self.store_records:
            self.violation[store_key] = []
            for product in self.store_records[store_key]:
                for i in range(len(policyBody_list)):
                    function_list[i](policyBody_list[i], product, store_key)

        # print(self.violation)


    def processOnePolicy(self, aPolicy, policyBody_list, function_list):
        """
        process one policy from the policy query
        store the policy function and corespondent policy body to put in the function
        """
        for key in aPolicy:
            # print(aPolicy[key])
            func = self.functions.get(key, self.invalidKey)
            function_list.append(func)
            policyBody_list.append(aPolicy[key])


    def mathComparison(self, policy_violation_msg, compareFunc, policy, product, store_key):
        """
        check the products with compare function function to see
        if the policy body key is comply with the compare function to compare value

        Will store the violation information into the violation field
        return true if product did not violate the policy, and false if it did violate
        """
        for key in policy: # example key = "sellPrice"
            if isinstance(policy[key], str):
                if not compareFunc(getattr(product, key), getattr(product, policy[key])): # example sellPrice < buyPrice
                    self.addInfoToViolation(policy_violation_msg, key, policy[key], product, store_key)
                    return False
            elif isinstance(policy[key], list):
                func = self.mathFuctions.get(policy[key][1], self.invalidMathKey)
                compare_value = func(product, policy[key][0], policy[key][2])
                if not compareFunc(getattr(product, key), compare_value): # example sellPrice < buyPrice + 10
                    self.addInfoToViolation(policy_violation_msg, key, policy[key], product, store_key)
                    return False
            else:
                if not compareFunc(getattr(product, key), policy[key]): # example sellPrice < 100
                    self.addInfoToViolation(policy_violation_msg, key, policy[key], product, store_key)
                    return False
            return True

    def greater(self, policy, product, store_key):
        """
        check the products with this function to see
        if the policy body key is greater than the compare value

        Will store the violation information into the violation field
        return true if product did not violate the policy, and false if it did violate
        """
        policy_violation_msg = " is not greater than "
        return self.mathComparison(policy_violation_msg, self.greaterThan, policy, product, store_key)
    
    def less(self, policy, product, store_key):
        """
        check the products with this function to see
        if the policy body key is less than the compare value

        Will store the violation information into the violation field 
        return true if product did not violate the policy, and false if it did violate
        """
        policy_violation_msg = " is not less than "
        return self.mathComparison(policy_violation_msg, self.lessThan, policy, product, store_key)

    def equal(self, policy, product, store_key):
        """
        check the products with this function to see
        if the policy body key is equal to the compare value

        Will store the violation information into the violation field 
        return true if product did not violate the policy, and false if it did violate
        """
        policy_violation_msg = " is not equal to "
        return self.mathComparison(policy_violation_msg, self.equalTo, policy, product, store_key)


    def bool(self, policy, product, store_key):
        """
        check the products with this function to see
        if the policy body key is set equal to the compare value

        Will store the violation information into the violation field 
        return true if product did not violate the policy, and false if it did violate
        """
        policy_violation_msg = " is not set to "
        for key in policy: # example key = "category_parent_HasProduct"
            if getattr(product, key) != policy[key]:
                self.addInfoToViolation(policy_violation_msg, key, policy[key], product, store_key)
                return False
            return True


    def format(self, policy, product, store_key):
        """
        check the products with this function to see
        if the policy body key is set to the require format

        Will store the violation information into the violation field 
        return true if product did not violate the policy, and false if it did violate
        """
        policy_violation_msg = " is not following the format "

        for key in policy: # example key = "supplier_createdDatetime"
            format = policy[key]
            productInput = getattr(product, key)
            if (len(format) != len(productInput)):
                self.addInfoToViolation(policy_violation_msg, key, policy[key], product, store_key)
                return False

            #loop over check instance of
            for i in range(len(format)): # ex. "0000-00-00 00:00:00"
                if (format[i].isdigit()):
                    if (not productInput[i].isdigit()):
                        self.addInfoToViolation(policy_violation_msg, key, policy[key], product, store_key)
                        return False
                elif (format[i].isalpha()):
                    if (not productInput[i].isalpha()):
                        self.addInfoToViolation(policy_violation_msg, key, policy[key], product, store_key)
                        return False
                else: # '-' ':' or other symbolic chars
                    if (productInput[i] != format[i]):
                        self.addInfoToViolation(policy_violation_msg, key, policy[key], product, store_key)
                        return False
            return True

    def exist(self, policy, product, store_key):
        """
        check the products with this function to see
        if the policy body key is exist/not exist in another store (an expensive check)

        return true or false for the if statement
        """
        policy_violation_msg = " is violating the existence requirement of: "
        
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
                self.addInfoToViolation(policy_violation_msg, key, policy[key], product, store_key)
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
                if (productAttr != [] or productAttr != ""):
                    policy_violation_msg = " enter should be null "
                    self.addInfoToViolation(policy_violation_msg, key, "", product, store_key)
                    return False
            else:
                if (productAttr == [] or productAttr == ""):
                    policy_violation_msg = " enter should not be null "
                    self.addInfoToViolation(policy_violation_msg, key, "", product, store_key)
                    return False
            return True

    def isComare(self, policy, product, store_key):
        """
        check the products with this function to see
        if the product attribute has the same string as in policy body 

        Will store the violation information into the violation field 
        return true if product did not violate the policy, and false if it did violate
        """
        key, val = policy.items()[0]
        return "not implemented"

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
        condBody_key, condBody_val = list(condition_body.items())[0]
        require_comparator, require_body = list(requirement.items())[0]

        condition_function = self.functions.get(condition_comparator, self.invalidKey)
        require_function = self.functions.get(require_comparator, self.invalidKey)
        append_Msg = " <due to if statemnt: " + condBody_key + " " + condition_comparator + " " + str(condBody_val) + ">"

        ## This part looks tricky cuz the function return ture/false and append violation msg at the same time
        ## need to refactor
        if condition_function(condition_body, product, store_key):  # condition fulfilled
            if not require_function(require_body, product, store_key): # requirement violated
                (self.violation[store_key])[-1] += append_Msg
        else:
            self.violation[store_key].pop()


    def greaterThan(self, left, right):
        return left + right

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

    def generateViolationInfo(self, msg, leftKey, rightKey, product):
        violation_msg = leftKey + msg + str(rightKey) + " Product ID: " + str(product.id)
        return violation_msg

    def addInfoToViolation(self, policy_violation_msg, key, policy_key, product, store_key):
        msg = self.generateViolationInfo(policy_violation_msg, key, policy_key, product)
        self.violation[store_key].append(msg)

    def invalidKey(self, policy, product, store_key):
        None
        #print("invalid key")

    def invalidMathKey(self, product, productKey, value):
        None
        #print("invalid math key")

