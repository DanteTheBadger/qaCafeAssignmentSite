import sqlite3 as sqlite
import requests
import json
import time

## Takes in an amount and then adds that many names to the db as customers
def addNames(amount):
    dbcon = sqlite.connect("qaCafeDatabase.db")

    dbcur = dbcon.cursor()

    requestURL = "https://scion.vampyrebytes.com/name/neutral/full"

    nameList = list(())
    for x in range(amount):
        response = requests.get(requestURL, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"})
        print(response.status_code)
        jsonText = json.loads(response.text)
        FullName = jsonText["name"]
        FullNameSplit = FullName.split(" ")
        nameList.append(FullNameSplit)
        time.sleep(1)


    for nameSet in nameList:
        queryString = f"INSERT INTO customer (firstName, lastName) VALUES ('{nameSet[0]}', '{nameSet[1]}');"
        dbcur.execute(queryString)
        # print(queryString)

    dbcon.commit()
    print("Finished Adding Names")

def addCoffees():
    dbcon = sqlite.connect("qaCafeDatabase.db")
    dbcur = dbcon.cursor()

    coffeeList = list(())
    coffeeList.append(("Mocha", 0.02))
    coffeeList.append(("Regular Coffee", 0.01))
    coffeeList.append(("Espresso", 0.05))

    for coffee in coffeeList:
        queryString = f"INSERT INTO coffees (coffeeName, pricePerML) VALUES ('{coffee[0]}', {coffee[1]})"
        dbcur.execute(queryString)

    dbcon.commit()

def addExtras():
    dbcon = sqlite.connect("qaCafeDatabase.db")
    dbcur = dbcon.cursor()

    extraList = list(())
    extraList.append(("Sugar", 0.01, "Grams"))
    extraList.append(("Milk", 0.05, "ML"))
    extraList.append(("Caramel Syrup", 0.1, "1 Large Measure"))

    for extra in extraList:
        queryString = f"INSERT INTO extras (extraName, costPerMeasure, measure) VALUES ('{extra[0]}', {extra[1]}, '{extra[2]}')"
        dbcur.execute(queryString)

    dbcon.commit()

def addCupSizes():
    dbcon = sqlite.connect("qaCafeDatabase.db")
    dbcur = dbcon.cursor()

    sizeList = list(())
    sizeList.append(("Espresso", 82))
    sizeList.append(("Small", 340))
    sizeList.append(("Medium", 455))
    sizeList.append(("Large", 568))
    for size in sizeList:
        queryString = f"INSERT INTO cupSizes VALUES ('{size[0]}', {size[1]});"
        dbcur.execute(queryString)

    dbcon.commit()

def addCupSizeRelations():
    dbcon = sqlite.connect("qaCafeDatabase.db")
    dbcur = dbcon.cursor()

    regularList = list(("Mocha", "Brewed Coffee"))
    sizeList = list(("Small", "Medium", "Large"))
    for drink in regularList:
        for size in sizeList:
            queryString = f"INSERT INTO cupCoffeeRelation (coffeeName, sizeName) VALUES ('{drink}', '{size}');"
            dbcur.execute(queryString)

    queryStringFinal = "INSERT INTO cupCoffeeRelation (coffeeName, sizeName) VALUES ('Espresso', 'Espresso');"
    dbcur.execute(queryStringFinal)

    dbcon.commit()

def addAvailableExtras():
    dbcon = sqlite.connect("qaCafeDatabase.db")
    dbcur = dbcon.cursor()

    extraList = list(())
    extraList.append(("Mocha", ("Caramel Syrup","Milk","Sugar")))
    extraList.append(("Brewed Coffee", ("Caramel Syrup","Milk","Sugar")))

    for drink in extraList:
        for extra in drink[1]:
            queryString = f"INSERT INTO coffeeExtrasAvl (coffeeName, extrasName) VALUES ('{drink[0]}', '{extra}')"
            dbcur.execute(queryString)

    dbcon.commit()


addAvailableExtras()