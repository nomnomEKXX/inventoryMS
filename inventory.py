import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from flask import Flask, request, jsonify

cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": "nomnom-db",
        "private_key_id": "d8d4891c11e74bf544eeadf17e6a5605d9577382",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCo+kUgAqCNm1j+\nc000e87vSjyi1Y5WfLx8v1ma8KrBbeJ3aNbV9iTeNqqIWAnr/qsC8ctxiO8FSBKp\naycpjRjWDpCVkE7V5FxUxOmyu9bB84FVS1Udr+u9d2/9gaZ2oia3xqzBYrh5fquM\n+fDUIdnB1Zy7A267xUGdLn4gw1xweELTDB7O58idF71sb1ipBVvy1EfWN1htJejU\nzMujQJK+gfijjYVujPYkNUp1cjQUGICVZj1JHEGVX5cvuMqtr9ij7biM1NPPpv3D\nMOhzKQLhgK/Ajo3T4uZfy5uOGzxPMQWuX6VGCcFSszvyALx6HHY5IDgU5bqQ1edd\nlf4qifedAgMBAAECggEALKbluU24a3MPkz2YuzO0PRta5pSUJlqT3EscPIs4NCD7\nZR55FtUSbP35FkpdZNVJD2AhqIDM2JJxC//au2ojk/0JS9x0WKUdmPDn6GkmmN3l\n4Uok1dF08/4pw82M1XCH1qxTXk7d/IzyfDBX6VaAmm3+GpUPn+LCMezlO3ckaDuQ\n6CgWLbp8u9gGMqQkxG3oqYUjtgeFjRXkw8ILIhn0pEPGBItMyQexK6pbPGeltkq5\nOcxvNtTm4SsqYgdx79Do2FUvFuwhHcz2Fugk6gg0dB8JHHamNlrG9SOsFw9Uwm2r\nYY1C4B6z1r0T8mY8mazID3qvsDxk/h93cYPlpWdIKQKBgQDivg3XdhJtXqTd8T9J\n6qcMafbB9xbAVrfjqnpd+9CVHtany6tyd9KlDhJEPINZhjoYynr/5mOKFz6SZdlG\n+u21s8l4Pu54lrDIG2z4mULMfAkNa7Be9thLLJ3Qefahfswyoqe26aeNbtQRZlqX\niw6mFp4dT7BZIhIEinUE33l8lwKBgQC+yBS+K4BDO4pJm7u6xYroVT+Zog7kHmug\nrisQjY1lgrCS+YIWcpEhWV+tdUp5BXsTUZ7M36FdcBXKcJ69Jzr8oi3l1cLCjUdl\nSS9J5wJo8nBfYARt/6WfqlgzSHsdDLqYGv5vtxgVtoGN8xA1E8/ZeS4999n6bAJG\nFpNQBD5P6wKBgCe+BjEQyfQPlbgtE9nB3lvHqu+efodh68Nk2yPkAlBQ4nDwuvFK\nXUp+5+a78I3dgAteWibGXAYVQutoHKhbTRT/GT4RUb0jNIMug3AjdNjgmLmYeYZ7\nn7e1b0feSMNPtTze06S02aBpn5QZK6HKRtwHtNkQYamN1jijiBU9kk6rAoGBAKAz\ncvedn77VKHJXC3TynIory5Q+uTJlOQtcNV1Y//rVm2BPlCU1XxkZ63XEoByvtYGr\ncCWpQ98qV6H+n81GPAoYRWJR9ZFZATLUGZl9GlD2A9aS0iVsHq/MYvPtUTQ7lBRV\n1oIIxXi2IGQKTvnDAS4ky+fNUIUwXVhtbJYsegaxAoGANUKGJmOMOSIbDjwgexva\n+bjVnQGUthCV/x/UqeFMdOKM2doPu78uQWXG9u7nxN63b3FWlCuKHnjq7nA5zEhz\nNWf50KWtQ2BIaGvAQJhw+ti9CuVi18WOM0nXfRjI/+0YsLcWQIZjKAIcvc83cwjX\nSOvsvytCXrSg65ayi7xb9t0=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-bhktu@nomnom-db.iam.gserviceaccount.com",
        "client_id": "108783214540036148659",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-bhktu%40nomnom-db.iam.gserviceaccount.com",
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
@app.route("/inventory/update/<userEmail>", methods=["POST", "GET"])
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
    app.run(host='0.0.0.0', port=5000, debug=True)

