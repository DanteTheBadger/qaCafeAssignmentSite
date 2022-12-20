from flask import Flask
from Database.DataBaseApp import DataBaseController

def main():
    dataBaseController = DataBaseController("DatabaseFile/qaCafeDatabase.db")
    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"



    app.run()

main()