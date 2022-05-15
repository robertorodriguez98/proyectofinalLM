import requests

def peticion(params):
    response = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php?'+ params)
    return response.json()

def imprimir(carta):
    for elem in carta.get("data"):
        print ("nombre: ",elem.get("name"))
        print ("tipo: ",elem.get("type"))
        print ("descripción: ",elem.get("desc"))
        print ("atk: ",elem.get("atk"))
        print ("def: ",elem.get("def"))
        print ("precio: ",elem.get("card_prices").get("cardmarket_price"),"€")

