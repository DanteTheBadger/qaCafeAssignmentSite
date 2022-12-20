import sqlite3 as sqlite
class DataBaseController:
    def __init__(self, databaseLocationString):
        self.dbConnectionString = databaseLocationString

    # All Case Execution Query
    def executeQuery(self, queryString, commit=False):
        dbConnection = sqlite.connect(self.dbConnectionString)
        with dbConnection:
            dbCur = dbConnection.cursor()
            queryResult = dbCur.execute(queryString)
            if commit == True:
                dbConnection.commit()
        return queryResult
    
    # Reading Data
    def ReadAllCustomers(self):
        return self.executeQuery("Select * From Customer;")

    def ReadAllOrders(self):
        return self.executeQuery("Select * From customerOrders;")
    
    def ReadOrderByID(self, orderID):
        queryString = f"""
        SELECT customerOrders.orderID, orderCoffees.orderCoffeeID, orderCoffees.coffeeName, orderCoffees.cupName
        FROM customerOrders, orderCoffees
        WHERE customerOrders.orderID == orderCoffees.orderID
        AND customerOrders.orderID == {orderID};"""
        return self.executeQuery(queryString)

    # Creating an Order
    def CreateOrder(self, customerID):
        queryString = f"INSERT INTO customerOrders (customerID) VALUES ({customerID});"
        return self.executeQuery(queryString, True)

    # Adding Updating or Deleting a Coffee From and Order
    def AddCoffeeToOrder(self, orderID, coffeeName, cupSize):
        queryString = f"INSERT INTO orderCoffees (orderID, coffeeName, cupName) VALUES ({orderID}, '{coffeeName}', '{cupSize}');"
        return self.executeQuery(queryString, True)

    def UpdateCoffeeSize(self, orderCoffeeID, newCupSize):
        updateQueryString = f"UPDATE orderCoffees SET cupName = '{newCupSize}' WHERE orderCoffeeID == {orderCoffeeID};"
        self.executeQuery(updateQueryString, True)
    
    def deleteCoffeeFromOrder(self, orderCoffeeID):
        firstDelete = f"DELETE FROM extrasToOrderCoffee WHERE orderCoffeeID = {orderCoffeeID};"
        secondDelete = f"DELETE FROM orderCoffees WHERE orderCoffeeID = {orderCoffeeID};"
        self.executeQuery(firstDelete, True)
        self.executeQuery(secondDelete, True)

    # Managing Addons to the Coffees
    def AddExtraToCoffee(self, orderCoffeeID, extraName, amount):
        queryString = f"INSERT INTO extrasToOrderCoffee (orderCoffeeID, extraName, amount) VALUES ({orderCoffeeID}, '{extraName}', {amount});"
        self.executeQuery(queryString, True)

    def removeExtraFromCoffee(self, extraCoffeeID):
        queryString = f"DELETE FROM extrasToOrderCoffee WHERE extraCoffeeID = {extraCoffeeID}"
        self.executeQuery(queryString, True)

    def updateExtraAmount(self, extraCoffeeID, amount):
        queryString = f"UPDATE extrasToOrderCoffee SET amount = {amount} WHERE extraCoffeeID = {extraCoffeeID}"
        self.executeQuery(queryString, True)
    
    def readCoffeeExtras(self, orderCoffeeID):
        queryString = f"SELECT extrasToOrderCoffee.extraName, extrasToOrderCoffee.amount FROM extrasToOrderCoffee WHERE extrasToOrderCoffee.orderCoffeeID = {orderCoffeeID}"
        return self.executeQuery(queryString)