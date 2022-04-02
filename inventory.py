import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from flask import Flask, request, jsonify

cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": "nomnominventory-aeb00",
        "private_key_id": "edb7a07dac0144b5fa99bdde427fd5ce5dcb4c9b",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCWEvDYy1ksbuZ8\nRfNgbJtHumRd7ymuKu+ubJSYXF3hMYuyY2aKrQ7jWYNvcOYQzcRRdrm7zhnYMcK6\nR8o6dx5kMFoq5lsv/NciGz6BPzmn+E/W2G0b5z71/n+HQBevjGwrDxCdLN1VJzE8\ne4/JMN4Sbk81Z1kx94+euwePzaNkOTMzU9zJIhJRuSZm7OXae4EEuEcfp1642dNd\nE+vuuIbpg8L3ElanpfkrvL4wHVPR++CrXY4ExoKHUXvPJJacCYYmCDnAySqldGEu\nwitJn31LYijYOJM4vUYKDzs71RLZQzahItHjyWoNhmqAZC7bNjRCaMRJcz6drmbE\nmrNjTtZJAgMBAAECggEAHr1ieAWvDlro+yuY3ndglyCmzlbewr4ouiGjjlHdKPNt\nGe0iY+Vu10LOmVUWyvpa7BTVlpJw2MfYiy+JTNB5eSwuS/tDUmEH8ASEmRTKSo2i\nTO+n6b9ENj8bACkwsNSik29Sh99YtsiAXVMx8JQB6OSPdPDmZEXBNVI6Ckqk3TJJ\n5HHwdMpo2ABGYv3SD999bqG5J89Jzgye9wyCngcPzxUGbW1CLmrL9le8PaD5wJr7\n4I/Q5jT8eQ5DvlG7qhhIZoROcBkrr3R/CYkxKlXmmK8zWownb4nQ06hAVC2LomrT\nrztZwrNaiTWj6228hoiTdtmQcEhG6UY7DMJyiIaLAQKBgQDKJ+eomIABzRL2lHoJ\nhkdMSCxKj1n9Cl5pqd+SJ4BSUHREuk1kr4HOO9rFjRejSMRnRejZXhBitKoObwHV\n1R/F66VYKmlF/5//w2pZLY6qJ7NIlHdmHCBm8HKYosgt6/ytKH+GoyobdoSorY3C\nWHP7mUjdZdQ6tyyeYps8TcHQ9QKBgQC+C86qcz+N4O2d6PKcmgxJNzkmLxyH33wU\ngAeeOvuG3VD9bYTgWsEb9tR/GD5NVxX6Pntj+7qma58/+h6YlH3+fxoqu8KHa4wY\nOg+bbMoEmL2Y/A9AHJbDE6Qv8FtQowHEeUQ6gflfIdXftJk/RVTLve4HC20khOvi\nQuxBel/LhQKBgA1LborB7LkxmWup/BSgRhQYMwF8R/jCM89TIqbj/iZrsBnM/sX+\nXNUJTqvrSYCtim0YReX1r7IuG3jzh/VeHMbRZoBT2bSGySjy2w2eV2GNVtcRHIEU\nnHTon0C2g9+xQ17H6Qsbs+s2cib9svLzCj2jqQ0WY0yxOzf3WCoxGuv5AoGAYKVA\nhA330/7+178PIfR1KwaaWYC70Z0lTIePWDhGkV8bQMXhPPbqHX54selyRYJz+r6r\noTzyvo8cfTyFMrLRIAsjE3hIhPV8WRWtuiyoz42dXZ9RYhkn0iy64mYpCejbjT7e\nI6LVXjumuAzvoe1wIeyEj7CP4HJ4Qqgl3WaOMMECgYBrdI6V5oAuouVV/IsDsuUk\nVXd7XEF/VNUvdr6sPGj7PAjBtRlot+P2SEdg204AAIRi5yxENYi1V/C2BfHVLF3n\nxOM0hUXfwdw7Uq+tQhmZkkrgT/VBu5rLSyuL1mRL275H9S87KzhbrMNv5dBLmuFo\nSySY0Dyo8pAQGZ8oMFelXw==\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-v44zm@nomnominventory-aeb00.iam.gserviceaccount.com",
        "client_id": "101195053370382275550",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-v44zm%40nomnominventory-aeb00.iam.gserviceaccount.com",
    }
)

firebase_admin.initialize_app(cred)

db = firestore.client()
app = Flask(__name__)

# RETRIEVE INVENTORY
@app.route("/inventory/<userEmail>")
def getInventory(userEmail):
    try:
        userInventory = db.collection("inventory").document(userEmail).get().to_dict()
    except:
        return {"code": 401, "message": "Error occured retrieving inventory"}

    return {"code": 201, "data": userInventory}


# CREATE INVENTORY FOR NEW USER
@app.route("/inventory/add/<userEmail>")
def addInventory(userEmail):
    data = request.get_json()
    try:
        db.collection("inventory").document(userEmail).set(data)
    except:
        return {"code": 400, "message": "Error occured when creating inventory"}

    return {"code": 200, "message": "Inventory Created"}


# UPDATE / ADD EXISTING INVENTORY
@app.route("/inventory/update/<userEmail>", methods=["POST", "GET", "PUT"])
def updateInventory(userEmail):
    newFoods = request.get_json()
    # newFoods = {
    #     "gyoza": {
    #         "item_quantity": 6,
    #         "food_desc": "Yummy Gyoza",
    #         "food_name": "Fried Gyozas",
    #         "image": "https://images.unsplash.com/photo-1609183590563-7710ba1f90a9?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
    #         "old_price": "$6.00",
    #         "current_price": "$3.00",
    #     },
    #     "dog": {
    #         "item_quantity": 10,
    #         "food_desc": "Delicious Dog",
    #         "food_name": "Fried dog",
    #         "image": "https://images.unsplash.com/photo-1618173745201-8e3bf8978acc?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=930&q=80",
    #         "old_price": "$10.00",
    #         "current_price": "$5.00",
    #     },
    #     "cat": {
    #         "item_quantity": 10,
    #         "food_desc": "Delicious cat",
    #         "food_name": "Fried cat",
    #         "image": "https://images.unsplash.com/photo-1618173745201-8e3bf8978acc?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=930&q=80",
    #         "old_price": "$10.00",
    #         "current_price": "$10.00",
    #     },
    # }

    successUpdate = ""
    successAdd = ""
    message = ""

    userInventory = db.collection("inventory").document(userEmail).get().to_dict()
    invSnap = db.collection("inventory").document(userEmail)

    for food_name, foodDetails in newFoods.items():
        # UPDATE DISH
        if food_name in userInventory.keys():
            try:
                invSnap.update({food_name: foodDetails})
                successUpdate += food_name + ", "
            except:
                return {
                    "code": 400,
                    "message": "Failed to Update {} details".format(food_name),
                }
        # NEW DISH
        else:
            try:
                invSnap.update({food_name: foodDetails})
                successAdd += food_name + ", "
            except:
                return {
                    "code": 400,
                    "message": "Failed to Add {} details".format(food_name),
                }

    if successUpdate and successAdd:
        message += (
            "Sucessfully updated details of {}. Succesfully added details of {}".format(
                successUpdate[:-2], successAdd[:-2]
            )
        )
    elif successUpdate:
        message += "Sucessfully updated details of {}".format(successUpdate[:-2])
    else:
        message += "Succesfully added details of {}".format(successAdd[:-2])

    return {"code": 201, "message": message}


# DELETE FOOD
@app.route("/inventory/delete/<userEmail>", methods=["DELETE"])
def deleteInventory(userEmail):
    # target = {
    #     "gyoza": {
    #         "item_quantity": 6,
    #         "food_desc": "Yummy Gyoza",
    #         "food_name": "Fried Gyozas",
    #         "image": "https://images.unsplash.com/photo-1609183590563-7710ba1f90a9?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
    #         "old_price": "$6.00",
    #         "current_price": "$3.00",
    #     }
    # }

    target = request.get_json(())
    userInventory = db.collection("inventory").document(userEmail).get().to_dict()
    dbSnap = db.collection("inventory").document(userEmail)
    targetItem = list(target.keys())[0]

    if targetItem in userInventory:
        try:
            dbSnap.update({targetItem: firestore.DELETE_FIELD})

        except:
            return {"code": 400, "message": "Failed to delete {}".format(targetItem)}

    else:
        return {"code": 200, "message": "SPAM, DELETED"}

    return {"code": 200, "message": "{} Successfully Deleted".format(targetItem)}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
