from flask import Flask, render_template, url_for
from Database.DataBaseApp import DataBaseController

def main():
    dataBaseController = DataBaseController("DatabaseFile/qaCafeDatabase.db")
    app = Flask(__name__)

    @app.route("/")
    def homePage():
        return render_template('base.html')
    
    @app.route("/Customers")
    def customerPage():
        customerData = dataBaseController.ReadAllCustomers().fetchall()
        clientList = list()
        for result in customerData:
            customerProfile = (result[0], result[1], result[2])
            clientList.append(customerProfile)
        return render_template('customer.html', customerData=clientList)



    app.run(debug=True)

main()