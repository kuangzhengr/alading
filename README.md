# alading
This program is use to check if the product information is following the policy setup by the operator.

To run the prorgram:
The main.py is the main program, it will loop through each product data file(each file serves as a store record) saved in the "productData" folder.

How the program work:
After the program finished one check, and before it starts the next checking, it will sleep for some interval to allow any update for product data and policy.
The sleep interval and the checking policy query is stored in "query_interval" folder.

Each component's job:
Product.py: This is the data format for a single product when parsing from json.

DataParsing.py: This file contains function to fetch product data(in reallife situation it suppose to fetch from POS machine but here we just fetch from a folder). After fetching the data, it can parse all the products into the format introduced in Product.py, and then saves them under each store.

DataChecking.py: This file contains functions to apply all the policy check on every product. Whenever a violation is found, it will save the violation information.

Notifyer.py: This file contains function to send notify emails base on violation information.

main_controller.py: This is the main coordinator to intergrate all the functions in each file and make them work as a whole. The basic procedures are "Fetch data/interval/policy query -> Parse Data -> Check data -> Send notification -> Sleep for some interval"

main.py: There are two independent threads running in parallel. One simply contains a while loop to run the procedure introduced in main_controller.py. The other thread sets up a server to allow remote check from another computer to see if the program is running(here I only set up a local host as a mock).

Tests:
All the testing are containing in tests folder.

Addition program:
In programStatus_monitor folder contains a program to remotly check if the checking program is running.
Run the main.py, it will keep checking for some interval to see if the program is running.
The way it checks is to send a get request to the server and see if it returns a response with status code of 200.
If the program is not running(not getting a 200 response), it will send a email to notify the system operator.
Tests are in the same folder.
