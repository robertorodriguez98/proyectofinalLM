from funciones import *
#response = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Cannon Soldier MK-2')

print("######################################")
print("Mostrar la carta cuyo nombre es Raigeki")
carta=peticion('name=Raigeki')
imprimir(carta)
print("######################################")
print("Mostrar Las cartas que contienen mage en el nombre y tienen un ataque igual o inferior a 100")
carta=peticion('fname=mage&atk=lte100')
imprimir(carta)
print("######################################")
print("Mostrar las cartas que valen entre 100 y 120")
