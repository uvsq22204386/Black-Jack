from random import*
from tkinter import*

def main():
    couleurs = ["Coeur","Carreau","Pique","Trèfle"]
    rangs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valet', 'Reine', 'Roi', 'As']
    paquet = []

    for rang in rangs:
        for couleur in couleurs:
            paquet.append((rang,couleur))

    shuffle(paquet)

    paquet,main_joueur,main_banque = distribution(paquet)

    print("joueur",main_joueur,"banque",main_banque)

    etat = "en jeu"
    etape = "choix_du_joueur"

    while etat == "en jeu":
        while etat == "en jeu" and etape == "choix_du_joueur":
            choix = input()
            if choix == "tirer":
                paquet,main_joueur = tirer(paquet,main_joueur)
                print("joueur",main_joueur)
                etat = verification(main_joueur)
            elif choix == "rester":
                etape = "tirage_banque"
        while etat == "en jeu" and etape =="tirage_banque":
            if calcul_score(main_banque) < 17:
                tirer(paquet,main_banque)
                print("banque :",main_banque)
            else:
                etape = "comparaison"
        if calcul_score(main_joueur)>calcul_score(main_banque) and verification(main_joueur) != "perdu":
            print("c'est gagné")
            etat = "fin de jeu"
        elif calcul_score(main_joueur) == calcul_score(main_banque):
            print("égalité")
            etat = "fin de jeu"
        elif calcul_score(main_joueur) < calcul_score(main_banque):
            print ("c'est perdu")
            etat = "fin de jeu"

    if verification (main_joueur) == "perdu":
        print(main_joueur,"\n","c'est perdu")




def distribution (paquet):

    main_joueur = []
    main_banque = []
    main_joueur.append(paquet.pop())
    main_banque.append(paquet.pop())
    main_joueur.append(paquet.pop())
    main_banque.append(paquet.pop())
    return paquet, main_joueur , main_banque

def tirer (paquet, main):
    main.append(paquet.pop())
    return paquet, main

def verification(main):
    if calcul_score(main) > 21:
        return "perdu"
    else:
        return "en jeu"
    

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

banque = Canvas(bg = "#{:02x}{:02x}{:02x}".format(16, 180, 8),height = 700, width = 300,relief = "ridge",highlightcolor="red")
joueur = Canvas(bg = "#{:02x}{:02x}{:02x}".format(16, 180, 8),height = 700, width = 300, relief = "ridge",highlightcolor="red")
distribuer = Button(text="Distribuer")
tirer1 = Button(text = "Tirer")
rester1 = Button(text = "Distribuer")

banque.grid(column = 0, row = 0, rowspan = 5)
joueur.grid(column = 2, row = 0, rowspan = 5)
distribuer.grid(column  = 1,row = 2)
tirer1.grid(column = 0, row = 6 )
rester1.grid(column = 2, row = 6)


racine.mainloop()


