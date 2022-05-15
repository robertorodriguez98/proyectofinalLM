from funciones import *
#response = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Cannon Soldier MK-2')

print("######################################")
print("Mostrar la carta cuyo nombre es Raigeki")
carta=peticion('name=Raigeki')
imprimir(carta)
print("######################################")