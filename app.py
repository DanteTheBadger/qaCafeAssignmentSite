from flask import Flask, render_template, url_for, request, make_response
from Database.DataBaseApp import DataBaseController

def main():
    dataBaseController = DataBaseController("DatabaseFile/qaCafeDatabase.db")
    app = Flask(__name__)

    @app.route("/")
    def homePage():
        return render_template('base.html')
    
    @app.route("/Customer")
    def customerPage():
        customerData = dataBaseController.ReadAllCustomers().fetchall()
        clientList = list()
        for result in customerData:
            customerProfile = (result[0], result[1], result[2])
            clientList.append(customerProfile)
        return render_template('customer.html', customerData=clientList)

    @app.route("/Customer/<CustomerID>")
    def customerProfile(CustomerID):
        customerProfile = dataBaseController.GetCustomerById(CustomerID).fetchone()
        return render_template('customerProfile.html', customerData = customerProfile)

    # Order Management Code
    def createOrderOverview():
        orderList = dataBaseController.ReadAllOrders().fetchall()
        orderListFinal = list(())
        for order in orderList:
            # Getting Customer Name and Information
            customerData = dataBaseController.GetCustomerById(order[1]).fetchone()
            customerName = f"{customerData[1]} {customerData[2]}"
            customerData = list((customerData[0], customerName))
            # Getting Drink Information
            orderDrinks = dataBaseController.ReadOrderByID(order[0]).fetchall()
            orderInformation = list((order[0], customerData, orderDrinks))
            orderListFinal.append(orderInformation)
        return orderListFinal

    # Page for examining and managing orders (Still working on making it a one page deal. Maybe embed one page inside the other)
    @app.route("/Orders")
    def orders():
        orderInformation = createOrderOverview()
        return render_template('OrderOverview.html', orderData = orderInformation)
    # API Section for Orders so stuff can be messed with
    @app.route("/Orders/AddDrink")
    def addDrinkToOrder():
        error = None
        if request.method == "POST":
            print(request.form("DrinkName"))
            print(request.form("DrinkSize"))
        return {
            "ResponseCode" : 200,
            "DrinkAdded" : "MeNameGeoff"
        }
    @app.route("/Orders/EditDrink")
    def editDrink():
        print("Editing Drink")

    @app.route("/Orders/DeleteDrink")
    def deleteDrink():
        print("Deleting Drink")

    # API Section to build out live coffee list and which drinks have which sizes
    def buildCoffeeList():
        drinkDict = dict()
        coffeeList = dataBaseController.getCoffees().fetchall()
        for coffee in coffeeList:
            sizeList = dataBaseController.getSizeByCoffee(coffee[0])
            sizeListNew = list(())
            for size in sizeList:
                sizeListNew.append(size[0])
            coffeeName = str(coffee[0])
            drinkDict[coffeeName] = sizeListNew
        return drinkDict

    @app.route("/Drinks/GetAll")
    def getAllDrinks():
        return buildCoffeeList()

    # Testing Page
    @app.route("/test")
    def test():
        return render_template("test.html")

    # App Run
    app.run(debug=True)

main()