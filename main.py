from random import*
from tkinter import*
from tkinter import messagebox
from PIL import Image, ImageTk
from time import*

couleurs = ["Trèfle","Carreau","Coeur","Pique"]
rangs = ['As','2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valet', 'Reine', 'Roi']
paquet = []


# création du paquet en associant chaque rang (ex : as) à une couleur (ex : trèfle) : création de couples dans une liste :
for couleur in couleurs:
    for rang in rangs:
        paquet.append((rang,couleur))  

image = Image.open("C:\\Users\\quent\\OneDrive\\Bureau\\BlackJack\\cartes.png") # image contenant les 53 cartes (carte face cachée  + 52 cartes) les unes sous les autres

carte_cachée_dim = (0,0,110,170) # définition des dimensions, ie : coordonnées du coin haut gauche : x = 0 et y +0 et coordonnées du coin bas droite : x = 110 (largeur d'une carte) et y = 170 (longueur d'une carte)
carte_cachée = image.crop(carte_cachée_dim) # recadrage en fonction des dimensions


carte_largeur = image.width # définition de la largeur d'une carte : largeur de l'image car les cartes sont les unes sous les autres 
carte_hauteur = image.height // 53 # définition de la longueur d'une carte : longueur de l'image divisé par 53 car il y a 53 cartes les unes sous les autres

cartes = []

# boucle pour recadrer les 52 cartes restantes de l'image (sans celle face cachée) :
for i in range(52): 

    carte_x = 0 # définition de l'abscisse (reste la même pour chaque carte car le coin haut droite est toujours sur l'extrémité gauche de l'image, et inversement pour coin bas droite)
    carte_y = i * carte_hauteur + 170 # définition de l'ordonnée, part de 170 pour la première carte car la première carte est la carte face cachée donc on part de la deuxième
    carte_dim = (carte_x, carte_y, carte_x + carte_largeur, carte_y + carte_hauteur) # définition des dimensions 
    carte = image.crop(carte_dim) # recadrage
    cartes.append(carte) # ajout des images des cartes dans une liste : les images sont dans le même ordre que les cartes dans la liste "paquet"

cartes_et_images = list(zip(paquet,cartes)) # création d'une liste associant : rang, couleur et image de la carte

shuffle(cartes_et_images) # mélange la liste (paquet + image)

paquet,cartes = list(zip(*cartes_et_images)) # redivision de la liste paquet et image qui sont donc mélangées dans le même ordre 

paquet = list(paquet)
cartes = list(cartes)

# initialisation des variables utilisées :
place_carte_joueur = 0
place_carte_banque = 0

carte_image_en_jeu_joueur= []
carte_image_en_jeu_banque = []

main_banque = []
main_joueur = []

benefice = 0

cash = 500
mise = 0 

jeu_split = False # cette variable permet de savoir si le joueur à activer la fonction split
premiere_main = 0 # permet de garder en mémoire le score de la première main lors du split
plus_de_21 = 0

def distribuer ():
    '''Cette fonction a pour but de distribuer les cartes initiales de la banque et du joueur en début de partie'''
    global paquet, main_joueur, main_banque,joueur_valeur,banque_valeur,place_carte_joueur,place_carte_banque,carte_image_en_jeu_joueur,carte_image_cachée,Score_banque, Score_joueur,benefice
    
    # Distribution première carte au joueur :
    main_joueur.append(paquet.pop()) # rajout à la main de la dernière carte du paquet plus supression de cette carte du paquet
    carte_image = ImageTk.PhotoImage(cartes.pop()) # définition de la denière image du paquet pour que tkinter puisse l'utilitser
    carte_image_en_jeu_joueur.append(carte_image) # ajout de cette image à la liste contenant toutes les images des cartes du joueur
    
    # Distribution première carte à la banque :
    main_banque.append(paquet.pop())
    carte_image = ImageTk.PhotoImage(cartes.pop())
    carte_image_en_jeu_banque.append(carte_image)
    
    # Distribution deuxième carte au joueur :
    main_joueur.append(paquet.pop())
    carte_image = ImageTk.PhotoImage(cartes.pop())
    carte_image_en_jeu_joueur.append(carte_image)
    
    # Calcul de la valeur des mains : 
    joueur_valeur = calcul_score(main_joueur)
    banque_valeur = calcul_score(main_banque)
    
    # Affichage
    for i in range (len(carte_image_en_jeu_joueur)):
        tapis.create_image(300+place_carte_joueur,600,image = carte_image_en_jeu_joueur[i], tags = ("carte", "split"))
        place_carte_joueur+=55 
    
    for i in range (len(carte_image_en_jeu_banque)):
        tapis.create_image(300+place_carte_banque,300,image = carte_image_en_jeu_banque[i] , tags = "carte")
    
    carte_image_cachée = ImageTk.PhotoImage(carte_cachée)
    tapis.create_image(300 + 55,300,image = carte_image_cachée, tag = "carte")
    
    if etat_affich_valeur == True:
        Score_banque.config (text =  "Score : " + str(banque_valeur))
        Score_joueur.config (text = "Score : " + str(joueur_valeur))
    
    if calcul_score(main_joueur) == 21:
        messagebox.showinfo("Fin de partie","Résultat : gagné")
        benefice = 2*mise + mise//2

def tirer ():
    global paquet,main_joueur, joueur_valeur,carte_image,place_carte_joueur,carte_image_en_jeu_joueur,Score_joueur, plus_de_21
    
        
    main_joueur.append(paquet.pop())
    joueur_valeur = calcul_score(main_joueur)
        
    carte_image = ImageTk.PhotoImage(cartes.pop())
    carte_image_en_jeu_joueur.append(carte_image)
        
    for i in range (len(carte_image_en_jeu_joueur)):
        tapis.create_image(300+place_carte_joueur,600,image = carte_image_en_jeu_joueur[i], tags= ("carte","split"))
    place_carte_joueur += 55
    
    if etat_affich_valeur == True:
                    Score_joueur.config (text = "Score : " + str(joueur_valeur))

    if jeu_split == False : 
        if joueur_valeur > 21:
                messagebox.showinfo("Fin de partie","Résultat : perdu")

        elif joueur_valeur == 21:
                rester()
    else: 
        if joueur_valeur>21:
            if jeu_split == "deuxieme_main":
                if plus_de_21 == True and calcul_score(main_joueur) > 21:
                    messagebox.showinfo("Fin de partie","Résultat : \n" + "Première main : c'est perdu \n" + "Deuxième main : c'est perdu")
                else:
                    rester()
            else:
                if calcul_score(main_joueur) > 21:
                    plus_de_21 = True
                tapis.after(1500, main2_split)
        


def rester ():
    global paquet,banque_valeur,carte_image_en_jeu_banque,place_carte_banque,Score_banque,benefice,premiere_main
    if jeu_split != True:
        while banque_valeur<17:
            main_banque.append(paquet.pop())
            carte_image = ImageTk.PhotoImage(cartes.pop())
            carte_image_en_jeu_banque.append(carte_image)

            banque_valeur = calcul_score(main_banque)
        
        if etat_affich_valeur == True:
                Score_banque.config (text =  "Score : " + str(banque_valeur))
            

        for i in range (len(carte_image_en_jeu_banque)):
            tapis.create_image(300+place_carte_banque,300,image = carte_image_en_jeu_banque[i], tags = "carte")
            place_carte_banque+=55

        if premiere_main == 0:
            if banque_valeur > 21 or joueur_valeur>banque_valeur:
                messagebox.showinfo("Fin de partie","Résultat : gagné")
                benefice = 2*mise
                
            elif banque_valeur>joueur_valeur:
                messagebox.showinfo("Fin de partie","Résultat : perdu")
                
            else: 
                messagebox.showinfo("Fin de partie","Résultat : égalité")
                benefice = mise

            
        else:
            if premiere_main > 21 or (banque_valeur > premiere_main and banque_valeur <= 21):
                resultat_premiere_main = "perdu"
            elif premiere_main == banque_valeur:
                resultat_premiere_main = "egalite"
            elif premiere_main > banque_valeur or banque_valeur > 21:
                resultat_premiere_main = "gagne"
            
            if joueur_valeur > 21 or (banque_valeur > joueur_valeur and banque_valeur <= 21):
                resultat_deuxieme_main = "perdu"
            elif joueur_valeur == banque_valeur:
                resultat_deuxieme_main = "egalite"
            elif joueur_valeur > banque_valeur or banque_valeur > 21:
                resultat_deuxieme_main = "gagne"

            if resultat_premiere_main == "gagne" and resultat_deuxieme_main == "gagne":
                messagebox.showinfo("Fin de partie","Résultat : \n" + "Première main : c'est gagné \n" + "Deuxième main : c'est gagné")
                benefice = 2*mise
            elif resultat_premiere_main == "gagne" and resultat_deuxieme_main == "egalite":
                messagebox.showinfo("Fin de partie","Résultat : \n" + "Première main : c'est gagné \n" + "Deuxième main : égalite")
                benefice = int(1.5*mise)
            elif resultat_premiere_main == "gagne" and resultat_deuxieme_main == "perdu":
                messagebox.showinfo("Fin de partie","Résultat : \n" + "Première main : c'est gagné \n" + "Deuxième main : c'est perdu")
                benefice = mise
            elif resultat_premiere_main == "egalite" and resultat_deuxieme_main == "gagne":
                messagebox.showinfo("Fin de partie","Résultat : \n" + "Première main : égalité \n" + "Deuxième main : c'est gagné")
                benefice = int(1.5*mise)
            elif resultat_premiere_main == "egalite" and resultat_deuxieme_main == "egalite":
                messagebox.showinfo("Fin de partie","Résultat : \n" + "Première main : égalité \n" + "Deuxième main : égalité")
                benefice = mise
            elif resultat_premiere_main == "egalite" and resultat_deuxieme_main == "perdu":
                messagebox.showinfo("Fin de partie","Résultat : \n" + "Première main : égalité \n" + "Deuxième main : c'est perdu")
                benefice = mise//2
            elif resultat_premiere_main == "perdu" and resultat_deuxieme_main == "gagne":
                messagebox.showinfo("Fin de partie","Résultat : \n" + "Première main : c'est perdu \n" + "Deuxième main : c'est gagné")
                benefice = mise
            elif resultat_premiere_main == "perdu" and resultat_deuxieme_main == "egalite":
                messagebox.showinfo("Fin de partie","Résultat : \n" + "Première main : c'est perdu \n" + "Deuxième main : égalité")
                benefice = mise//2
            elif resultat_premiere_main == "perdu" and resultat_deuxieme_main == "perdu":
                messagebox.showinfo("Fin de partie","Résultat : \n" + "Première main : c'est perdu \n" + "Deuxième main : c'est perdu")
    else: 
        main2_split()
    
    
        
def doubler():
    global cash, mise
    cash -= mise
    mise *= 2
    Cash.config(text = "Cash : " + str(cash))
    Mise.config(text = "Mise : " + str(mise))
    tirer()
    if joueur_valeur <= 21:
        rester()

def split():
    global place_carte_joueur,carte_image_en_jeu_joueur,carte_image_en_jeu_joueur2,carte, main_joueur,main_joueur2, jeu_split, mise,cash
    carte_image_en_jeu_joueur2 = []
    main_joueur2 =[]
    place_carte_joueur = 0
    main_joueur2.append(main_joueur.pop())
    carte_image_en_jeu_joueur2.append(carte_image_en_jeu_joueur.pop())

    jeu_split = True

    tapis.delete("split")
    
    for i in range (len(carte_image_en_jeu_joueur)):
        tapis.create_image(300+place_carte_joueur,600,image = carte_image_en_jeu_joueur[i], tags = "carte")
        place_carte_joueur+=55
    if etat_affich_valeur == True:
            Score_joueur.config (text = "Score : " + str(calcul_score(main_joueur)))

    cash -= mise
    mise *= 2
    Cash.config(text = "Cash : " + str(cash))
    Mise.config(text = "Mise de la première main : " + str(mise//2)+ "\n" + "Mise de la deuxième main : " + str(mise//2))
        
    
        
def main2_split():
    global main_joueur,main_joueur2,carte_image_en_jeu_joueur,carte_image_en_jeu_joueur2,place_carte_joueur,jeu_split,premiere_main
    premiere_main = calcul_score(main_joueur)
    main_joueur = main_joueur2.copy()
    carte_image_en_jeu_joueur = carte_image_en_jeu_joueur2.copy()
    tapis.delete("split")
    tapis.create_image(300,600,image = carte_image_en_jeu_joueur2[0], tags = "carte")
    place_carte_joueur = 55
    jeu_split = "deuxieme_main"

    if etat_affich_valeur == True:
            Score_joueur.config (text = "Score : " + str(calcul_score(main_joueur)))

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

def rejouer():
    global place_carte_banque,place_carte_joueur,carte_image_en_jeu_banque,carte_image_en_jeu_joueur, Score_banque, main_joueur,main_banque,mise,cash,benefice

    tapis.delete("carte")
    Score_banque.config(text ="")
    Score_joueur.config(text = "")
    
    main_joueur = []
    main_banque = []

    place_carte_joueur = 0
    place_carte_banque = 0
    
    carte_image_en_jeu_joueur= []
    carte_image_en_jeu_banque = []

    mise = 0
    cash += benefice
    benefice = 0

    Mise.config(text = "Mise : 0")
    Cash.config (text = "Cash : " + str(cash + benefice))



def mise_de_10():
    global cash,mise
    mise += 10
    cash -= 10
    Cash.config(text = "Cash : " + str(cash))
    Mise.config(text = "Mise : " + str(mise))


etat_affich_valeur = False         

def affich_valeur():
    global etat_affich_valeur
    if valeur.get() == 1:
        etat_affich_valeur = True
        Score_banque.config(text = "Score : " + str(calcul_score(main_banque)))
        Score_joueur.config(text = "Score = " + str(calcul_score(main_joueur)))
    else:
        etat_affich_valeur = False
        Score_banque.config(text = "")
        Score_joueur.config(text = "")

racine = Tk()

tapis = Canvas(bg = "#{:02x}{:02x}{:02x}".format(35, 90, 78), height = 800, width = 900, highlightbackground="#{:02x}{:02x}{:02x}".format(156, 28, 30), highlightthickness=4, relief="ridge")


Tirer = Button(tapis, text="Tirer", command = tirer)
Rester = Button(tapis, text="Rester", command = rester)
Distribuer = Button(tapis, text="Distribuer", command = distribuer)
Rejouer = Button(tapis, text = "Rejouer", command = rejouer )

Doubler = Button(tapis,text = "Doubler",command = doubler)
tapis.create_window(600,750, window = Doubler)

Split = Button(tapis, text = "Split", command = split)
tapis.create_window(700,750, window = Split)


jeton = PhotoImage(file="C:\\Users\\quent\\OneDrive\\Bureau\\BlackJack\\jeton1.png")
Jeton = Button(tapis, image = jeton, command = mise_de_10)
Jeton.configure(bg = "#{:02x}{:02x}{:02x}".format(35, 90, 78),relief = "flat", activebackground= "#{:02x}{:02x}{:02x}".format(35, 90, 78),borderwidth=0)

tapis.create_window(100,500, window = Jeton)



tapis.create_rectangle(243,213,797,387, width = 4, outline = "#{:02x}{:02x}{:02x}".format(156, 28, 30))
tapis.create_rectangle(243,513,797,687, width = 4, outline = "#{:02x}{:02x}{:02x}".format(156, 28, 30))

valeur = IntVar()
valeur_ou_non = Checkbutton(tapis, bg = "#{:02x}{:02x}{:02x}".format(35, 90, 78),activebackground = "#{:02x}{:02x}{:02x}".format(35, 90, 78) , text = "Afficher la valeur des mains", variable = valeur, command = affich_valeur)
tapis.create_window(815,789, window  = valeur_ou_non)

Score_banque = Label(tapis, bg = "#{:02x}{:02x}{:02x}".format(35, 90, 78), text = "")
tapis.create_window(100,300, window = Score_banque)

Score_joueur = Label(tapis, bg = "#{:02x}{:02x}{:02x}".format(35, 90, 78), text = "")
tapis.create_window(100,600, window = Score_joueur)

Cash = Label(tapis,bg = "#{:02x}{:02x}{:02x}".format(35, 90, 78), text = "Cash : " + str(cash) )
tapis.create_window(200,200, window = Cash)

Mise = Label(tapis,bg = "#{:02x}{:02x}{:02x}".format(35, 90, 78), text = "Mise : " + str(mise) )
tapis.create_window(500,75, window = Mise)

tapis.create_window(200, 750, window=Tirer)
tapis.create_window(400, 780, window=Rester)
tapis.create_window(600, 780, window=Distribuer)
tapis.create_window(600,700,window = Rejouer, tags = "Rejouer_bouton")


#tapis.itemconfigure("Rejouer_bouton", state ="hidden")

# tapis.create_rectangle(650,585,905,805, outline = "#{:02x}{:02x}{:02x}".format(156, 28, 30), width =4)
# tapis.create_rectangle(0,585,255,805, outline = "#{:02x}{:02x}{:02x}".format(156, 28, 30), width =4)

tapis.grid()


racine.mainloop()


