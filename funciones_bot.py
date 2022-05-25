import requests

def get_info(palabra):

    url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?name='+palabra
    print(url)
    response = requests.get(url)

# return a custom response if an invalid word is provided
    data = response.json()

    if type(data.get("error")) == str:
        error_response = 'La busqueda introducida no coincide con ningun elemento de la base de datos'
        return error_response


    else:
        return data["data"][0]