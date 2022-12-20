from flask import Flask, render_template, url_for
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
            print(order)
            # Getting Customer Name and Information
            customerData = dataBaseController.GetCustomerById(order[1]).fetchone()
            customerName = f"{customerData[1]} {customerData[2]}"
            customerData = list((customerData[0], customerName))
            # Getting Drink Information
            orderDrinks = dataBaseController.ReadOrderByID(order[0]).fetchall()
            print(f"{customerData} -- {len(orderDrinks)}")
            orderInformation = list((order[0], customerData, orderDrinks))
            orderListFinal.append(orderInformation)
        return orderListFinal


    @app.route("/Orders")
    def orders():
        orderInformation = createOrderOverview()
        return render_template('OrderOverview.html', orderData = orderInformation)

    @app.route("/AddDrink/<orderID>")
    def addDrink(orderID):
        return render_template('addDrink.html')


    # App Run
    app.run(debug=True)

main()