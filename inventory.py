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
@app.route("/inventory")
def getInventory():
    data = request.get_json()
    sellerID = data['storeID']
    try:
        check_doc = db.collection(u"inventory").document(sellerID).get()
        userInventory = db.collection("inventory").document(sellerID).get().to_dict()
    except:
        return {"code": 500, "message": "Error occurred retrieving inventory"}

    if check_doc.exists:
        return {"code": 200, "data": userInventory}

    return {"code": 404, "message": "Seller Does not Exist"}


# CREATE INVENTORY FOR NEW USER
@app.route("/inventory/add", methods=["POST", "GET", "PUT"])
def addInventory():
    data = request.get_json()
    # store_name = data['storeName']
    sellerID = data['storeID']
    newFoods = data["foodListings"]

    doc_ref = db.collection("inventory").document(sellerID)
    doc = doc_ref.get()

    # UPDATE THE EXISTING DOCUMENT
    if doc.exists:
        print("document exists")

        successUpdate = ""
        successAdd = ""
        message = ""

        userInventory = db.collection("inventory").document(sellerID).get().to_dict()
        invSnap = db.collection("inventory").document(sellerID)

        for food_name, foodDetails in newFoods.items():
            # UPDATE DISH
            if food_name in userInventory.keys():
                try:
                    invSnap.update({food_name: foodDetails})
                    successUpdate += food_name + ", "
                except:
                    return {
                        "code": 500,
                        "message": "Failed to Update {} details. Update terminated".format(
                            food_name
                        ),
                    }
            # NEW DISH
            else:
                try:
                    invSnap.update({food_name: foodDetails})
                    successAdd += food_name + ", "
                except:
                    return {
                        "code": 500,
                        "message": "Failed to Add {} details. Update terminated".format(
                            food_name
                        ),
                    }

        if successUpdate and successAdd:
            message += "Sucessfully updated details of {}. Succesfully added details of {}".format(
                successUpdate[:-2], successAdd[:-2]
            )
        elif successUpdate:
            message += "Sucessfully updated details of {}".format(successUpdate[:-2])
        else:
            message += "Succesfully added details of {}".format(successAdd[:-2])

        # fbMessage = { "message" : "" }

        # print("SEND TO FACEBOOK GRAPH API -1")
        # response = requests.post("http://proje-LoadB-1RCK4FEMDS4L6-5ad76914379a89cd.elb.us-east-1.amazonaws.com:4545/create_new_post", data = fbMessage )
        # print(f"FACEBOOK RESPONSE: {response}")

        return {"message": "Food has been restocked...nom nom nom"}
        # return str(response)

    # CREATE NEW DOCUMENT FOR INVENTORY
    else:
        try:
            db.collection("inventory").document(sellerID).set(data)
            foodLink = (
                f"https://nomnomis216.netlify.app/foodListings?shopName={sellerID}"
            )
            fbMessage = f"New food has been added! Check them out now with the link! {foodLink}"

            # postMessage = { "message" : fbMessage}

            # print("SEND TO FACEBOOK GRAPH API -2")
            # response = requests.post("http://proje-LoadB-1RCK4FEMDS4L6-5ad76914379a89cd.elb.us-east-1.amazonaws.com:4545/create_new_post", data = postMessage) 
            # print("FACEBOOK RESPONSE", response)

        except:
            return {"code": 500, "message": "Error occured when creating inventory"}

        # return str(response)
        return {"message": fbMessage}


# UPDATE / ADD EXISTING INVENTORY
@app.route("/inventory/update/<sellerID>", methods=["POST", "GET", "PUT"])
def updateInventory(sellerID):
    newFoods = request.get_json()
    # {
    #     "gyoza": {
    #         "counter": 6,
    #         "foodDesc": "Yummy Gyoza",
    #         "foodName": "Fried Gyozas",
    #         "image": "https://images.unsplash.com/photo-1609183590563-7710ba1f90a9?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
    #         "oldPrice": "$6.00",
    #         "price": "$3.00",
    #     },
    #     "dog": {
    #         "counter": 10,
    #         "foodDesc": "Delicious Dog",
    #         "foodName": "Fried dog",
    #         "image": "https://images.unsplash.com/photo-1618173745201-8e3bf8978acc?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=930&q=80",
    #         "oldPrice": "$10.00",
    #         "price": "$5.00",
    #     },
    #     "cat": {
    #         "counter": 10,
    #         "foodDesc": "Delicious cat",
    #         "foodName": "Fried cat",
    #         "image": "https://images.unsplash.com/photo-1618173745201-8e3bf8978acc?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=930&q=80",
    #         "oldPrice": "$10.00",
    #         "price": "$10.00",
    #     }
    # }

    successUpdate = ""
    successAdd = ""
    message = ""

    userInventory = db.collection("inventory").document(sellerID).get().to_dict()
    invSnap = db.collection("inventory").document(sellerID)

    for food_name, foodDetails in newFoods.items():
        # UPDATE DISH
        if food_name in userInventory.keys():
            try:
                invSnap.update({food_name: foodDetails})
                successUpdate += food_name + ", "
            except:
                return jsonify({
                    "code": 500,
                    "message": "Failed to Update {} details. Update terminated".format(
                        food_name
                    ),
                })

        # NEW DISH
        else:
            try:
                invSnap.update({food_name: foodDetails})
                successAdd += food_name + ", "
            except:
                return jsonify({
                    "code": 500,
                    "message": "Failed to Add {} details. Update terminated".format(
                        food_name
                    ),
                })

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

    return jsonify({"code": 200, "message": message})


# DELETE FOOD
@app.route("/inventory/delete/<sellerID>", methods=["DELETE"])
def deleteInventory(sellerID):
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
    userInventory = db.collection("inventory").document(sellerID).get().to_dict()
    dbSnap = db.collection("inventory").document(sellerID)
    targetItem = list(target.keys())[0]

    if targetItem in userInventory:
        try:
            dbSnap.update({targetItem: firestore.DELETE_FIELD})

        except:
            return {"code": 500, "message": "Failed to delete {}".format(targetItem)}

    else:
        return {"code": 200, "message": "SPAM, DELETED"}

    return {"code": 200, "message": "{} Successfully Deleted".format(targetItem)}


# ENDPT TAKE IN ORDER OBJECT AND COMPARE AGAINST DB TO SEE IF QTY IS SUFFICIENT


@app.route("/inventory/verify", methods=["GET", "POST", "PUT"])
def verifyOrder():
    
    #VARIABLE NAMES MAY BE WRONG, THE STRUCUTURE OF DATA ABIT WEIRD, I CHANGED STOREID TO EMAIL FIRST SINCE DB HAVENT CHANGE.
    # WHY GOT COUNTER AND QUANTITY 

    # data = {
    #     "order": {
    #         "status": "pending",
    #         "uid": "3",
    #         "subtotal": 69.50,
    #         "storeID": "matthias123@gmail.com",
    #         "collectionTime": "2:40pm",
    #         "cart": [
    #             {
    #                 "counter": 10,
    #                 "foodDesc": "pui",
    #                 "foodName": "dog",
    #                 "image": "NIL",
    #                 "oldPrice": "5.90",
    #                 "price": "8.90",
    #                 "quantity": 10,
    #                 "shopKey": "disdhjaidjowe",
    #             },
    #             {
    #                 "counter": 10,
    #                 "foodDesc": "pui",
    #                 "foodName": "gyoza",
    #                 "image": "NIL",
    #                 "oldPrice": "5.20",
    #                 "price": "6.20",
    #                 "quantity": 10,
    #                 "shopKey": "dsdsdwefefwef",
    #             },
    #         ],
    #     }
    # }

    data = request.get_json()
    # return data
    storeID = data["order"]["storeID"]
    print(storeID)
    userInventory = db.collection("inventory").document(storeID).get().to_dict()
    print(userInventory)
    # inventSnap = db.collection("inventory").document(storeID).get().to_dict()
    

    successMessage = ""
    failedMessage = ""

    cart = data["order"]["cart"]
    for item in cart:
        foodName = item["foodName"]

        orderedQuantity = item["quantity"]
        inventQuantity = userInventory['foodListings'][foodName]['counter']
        # inventQuantity = inventQuantity['counter']

        if orderedQuantity > inventQuantity:
            failedMessage += "Ordered Quantity for {} exceeded limit. Order Process TERMINATED".format(
                foodName
            )
            return jsonify({
                "response": "reject order",
                "code": 400, 
            })

        else:
            updatedQuantity = inventQuantity - orderedQuantity
            itemDict = userInventory['foodListings'][foodName]
            itemDict["counter"] = updatedQuantity
            newObject = {
                foodName : itemDict
            }

            try:
                # userInventory['foodListings'].update({itemDict["counter"]: updatedQuantity})
                db.collection("inventory").document(storeID).update({"foodListings": userInventory["foodListings"]})
                successMessage += "Succesfully ordered {} {}.".format(
                    orderedQuantity, foodName
                )

            except:
                return jsonify({
                    "response": "reject order",
                    "code": 500,
                })

    return {
        "response": "create order",
        "code": 200,
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5700, debug=True)
