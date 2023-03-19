from random import*
from tkinter import*
from PIL import Image


couleurs = ["Trèfle","Carreau","Coeur","Pique"]
rangs = ['As','2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valet', 'Reine', 'Roi']
paquet = []

for couleur in couleurs:
    for rang in rangs:
        paquet.append((rang,couleur))

# Ouvrir l'image PNG
# image = Image.open("C:\\Users\\quent\\OneDrive\\Bureau\\BlackJack\\cartes.png")

# # Déterminer la largeur et la hauteur de chaque carte
# carte_largeur = image.width
# carte_hauteur = image.height // 53

# # Initialiser une liste pour stocker les cartes
# cartes = []

# # Boucler à travers chaque carte et l'ajouter à la liste
# for i in range(52):
#     # Calculer les coordonnées de la carte actuelle
#     carte_x = 0
#     carte_y = i * carte_hauteur + 170
#     carte_box = (carte_x, carte_y, carte_x + carte_largeur, carte_y + carte_hauteur)
        
#     # Extraire la carte en tant qu'image séparée
#     carte = image.crop(carte_box)
        
#     # Ajouter la carte à la liste
#     paquet[i] = paquet[i] + (carte,)

shuffle(paquet)


def distribuer ():
    global paquet, main_joueur, main_banque,joueur_valeur,banque_valeur
    main_joueur = []
    main_banque = []
    main_joueur.append(paquet.pop())
    main_banque.append(paquet.pop())
    main_joueur.append(paquet.pop())
    joueur_valeur = calcul_score(main_joueur)
    banque_valeur = calcul_score(main_banque)
    joueur.config(text = "Main joueur : " + str(main_joueur))
    banque.config(text = "Main banque : " + str([main_banque,"face cachée"]))
    

def tirer ():
    global paquet,main_joueur, joueur_valeur
    main_joueur.append(paquet.pop())
    joueur_valeur = calcul_score(main_joueur)
    joueur.config(text = "Main joueur : " + str(main_joueur))
    if joueur_valeur > 21:
        print("perdu")
    elif joueur_valeur == 21:
        rester()

    
def rester ():
    global paquet,banque_valeur
    while banque_valeur<17:
        main_banque.append(paquet.pop())
        banque_valeur = calcul_score(main_banque)
        banque.config(text = "Main banque :"  + str(main_banque))
    if banque_valeur > 21 or joueur_valeur>banque_valeur:
        résultat.config(text = "Résultat : gagné")
    elif banque_valeur>joueur_valeur:
        résultat.config(text = "Résultat : perdu")
    else: 
        résultat.config(text = "Résultat : égalité")

    

def calcul_score(main):
    score = 0
    As = 0
    for card in main:
        if card[0] == "Valet" or card[0] == "Reine" or card [0] == "Roi":
            score +=10
        elif card[0] == "As":
            score += 11
            As += 1
        else:
            score+= int(card[0])
    while As>0 and score>21:
        As -=1
        score -=10
    return score

racine = Tk()

tapis = Canvas(bg = "#{:02x}{:02x}{:02x}".format(35, 90, 78), height = 800, width = 900, highlightbackground="#{:02x}{:02x}{:02x}".format(156, 28, 30), highlightthickness=3, relief="ridge")

Tirer = Button(tapis, text="Tirer", command = tirer)
Rester = Button(tapis, text="Rester", command = rester)
Distribuer = Button(tapis, text="Distribuer", command = distribuer)
joueur = Label(tapis, text = "Main joueur :")
banque = Label(tapis, text = "Main banque :")
résultat = Label(tapis, text = "Résultat :")
tapis.create_window(200, 750, window=Tirer)
tapis.create_window(400, 780, window=Rester)
tapis.create_window(600, 780, window=Distribuer)
tapis.create_window(200, 300, window=joueur)
tapis.create_window(200, 500, window = banque)
tapis.create_window(600,400, window = résultat)
tapis.grid()


racine.mainloop()


