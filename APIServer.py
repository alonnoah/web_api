from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from collections import namedtuple
import json
import requests

hostName = "localhost"
serverPort = 8080


def orderShop(category):
    lst = []
    dict = {"id": int,
            "name": str,
            "price": int}
    for inedx in category:
        dict["id"] = inedx.dishId
        dict["name"] = inedx.dishName
        dict["price"] = inedx.dishPrice
        lst.append(dict)
    return lst

class APIServer(BaseHTTPRequestHandler):
    lst= []
    url = "https://www.10bis.co.il/NextApi/GetRestaurantMenu?culture=en&uiCulture=en&restaurantId=19156&deliveryMethod=pickup"
    res = requests.post(url)

    def customResturantDecoder(resturantDict):
        return namedtuple('X', resturantDict.keys())(*resturantDict.values())

    json_loads = json.loads(res.text, object_hook=customResturantDecoder)
    categories = json_loads.Data.categoriesList
    for category in categories:
        lst.append(category.categoryName)
        if category.categoryName == "Pizza":
            order = orderShop(category.dishList)
        elif category.categoryName == "Drink":
            order = orderShop(category.dishList)
        elif category.categoryName == "Dessert":
            order = orderShop(category.dishList)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        if str(self.path) == "/drinks":
            # return drinks
            self.wfile.write(bytes("<p>drinks</p>", "utf-8"))
            pass
        elif str(self.path).startswith("/drink/"):
            # return drink
            self.wfile.write(bytes("<p>drink</p>", "utf-8"))
            pass
        elif str(self.path) == "/pizzas":
            # return pizzas
            self.wfile.write(bytes("<p>pizzas</p>", "utf-8"))
            pass
        elif str(self.path).startswith("/pizza/"):
            # return pizza
            self.wfile.write(bytes("<p>  </p>", "utf-8"))
            pass
        elif str(self.path) == "/desserts":

            # return desserts
            self.wfile.write(bytes("<p>desserts</p>", "utf-8"))
            pass
        elif str(self.path).startswith("/dessert/"):
            # return dessert
            self.wfile.write(bytes("<p>dessert</p>", "utf-8"))
            pass
        else:
            # no need
            pass
        
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), APIServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
