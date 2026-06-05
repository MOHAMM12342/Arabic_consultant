from dar_to_ar import *
from ar_to_dar import *

choix=int(input("taper 1 pour traduction darija-arabe\n2 pour traduction arabe-darija"))

if choix==1:
    prompt = input("entrer le texte en Darija à traduire : ")
    print("traduction en arabe : ", affichage(prompt))
else:
    prompt = input("entrer le texte en Arabe à traduire : ")
    print("traduction en Darija1 : ", fct(prompt))