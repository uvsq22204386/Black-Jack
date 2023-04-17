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

image = Image.open("cartes.png") # image contenant les 53 cartes (carte face cachée  + 52 cartes) les unes sous les autres

carte_cachée_dim = (0,0,110,170) # définition des dimensions, ie : coordonnées du coin haut gauche : x = 0 et y +0 et coordonnées du coin bas droite : x = 110 (largeur d'une carte) et y = 170 (longueur d'une carte)
carte_cachée = image.crop(carte_cachée_dim) # recadrage en fonction des dimensions
carte_cachée = carte_cachée.resize((143,221),Image.Resampling.LANCZOS)


carte_largeur = image.width # définition de la largeur d'une carte : largeur de l'image car les cartes sont les unes sous les autres 
carte_hauteur = image.height // 53 # définition de la longueur d'une carte : longueur de l'image divisé par 53 car il y a 53 cartes les unes sous les autres

cartes = []

# boucle pour recadrer les 52 cartes restantes de l'image (sans celle face cachée) :
for i in range(52): 

    carte_x = 0 # définition de l'abscisse (reste la même pour chaque carte car le coin haut droite est toujours sur l'extrémité gauche de l'image, et inversement pour coin bas droite)
    carte_y = i * carte_hauteur + 170 # définition de l'ordonnée, part de 170 pour la première carte car la première carte est la carte face cachée donc on part de la deuxième
    carte_dim = (carte_x, carte_y, carte_x + carte_largeur, carte_y + carte_hauteur) # définition des dimensions 
    carte = image.crop(carte_dim) # recadrage
    carte = carte.resize((143,221),Image.Resampling.LANCZOS)
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
    paquet_vide()

    main_joueur.append(paquet.pop()) # rajout à la main de la dernière carte du paquet plus supression de cette carte du paquet
    carte_image = ImageTk.PhotoImage(cartes.pop()) # définition de la denière image du paquet pour que tkinter puisse l'utilitser
    carte_image_en_jeu_joueur.append(carte_image) # ajout de cette image à la liste contenant toutes les images des cartes du joueur
    
    # Distribution première carte à la banque :
    paquet_vide()

    main_banque.append(paquet.pop())
    carte_image = ImageTk.PhotoImage(cartes.pop())
    carte_image_en_jeu_banque.append(carte_image)
    
    # Distribution deuxième carte au joueur :
    paquet_vide()

    main_joueur.append(paquet.pop())
    carte_image = ImageTk.PhotoImage(cartes.pop())
    carte_image_en_jeu_joueur.append(carte_image)

    # Calcul de la valeur des mains : 
    joueur_valeur = calcul_score(main_joueur)
    banque_valeur = calcul_score(main_banque)
    
    # Affichage
    for i in range (len(carte_image_en_jeu_joueur)):
        tapis.create_image(300+place_carte_joueur,545,image = carte_image_en_jeu_joueur[i], tags = ("carte", "split"))
        place_carte_joueur+=71 
    
    for i in range (len(carte_image_en_jeu_banque)):
        tapis.create_image(300+place_carte_banque,200,image = carte_image_en_jeu_banque[i] , tags = "carte")
    
    carte_image_cachée = ImageTk.PhotoImage(carte_cachée)
    tapis.create_image(300 + 55,200,image = carte_image_cachée, tag = "carte")
    
    if etat_affich_valeur == True:
        Score_banque.config (text =  "Score : " + str(banque_valeur))
        Score_joueur.config (text = "Score : " + str(joueur_valeur))
    
    if calcul_score(main_joueur) == 21:
        messagebox.showinfo("Fin de partie","Résultat : gagné")
        benefice = 2*mise + mise//2
        
        Tirer.configure(state = "disabled")
        Rester.configure(state = "disabled")
        Rejouer.configure(state = "active")

    Jeton.configure(state = "disabled")
    Distribuer.configure(state = "disabled")
    Tirer.configure(state = "active")
    Rester.configure(state = "active")
    Doubler.configure(state = "active")

    if main_joueur[0][0] == main_joueur[1][0]:
         Split.configure(state = "active")
    

def tirer ():
    global paquet,main_joueur, joueur_valeur,carte_image,place_carte_joueur,carte_image_en_jeu_joueur,Score_joueur, plus_de_21
    
    paquet_vide()

    main_joueur.append(paquet.pop())
    joueur_valeur = calcul_score(main_joueur)
        
    carte_image = ImageTk.PhotoImage(cartes.pop())
    carte_image_en_jeu_joueur.append(carte_image)
    

    for i in range (len(carte_image_en_jeu_joueur)):
        tapis.create_image(300+place_carte_joueur,545,image = carte_image_en_jeu_joueur[i], tags= ("carte","split"))
    place_carte_joueur += 71
    
    if etat_affich_valeur == True:
                    Score_joueur.config (text = "Score : " + str(joueur_valeur))

    if jeu_split == False : 
        if joueur_valeur > 21:
                messagebox.showinfo("Fin de partie","Résultat : perdu")
                Tirer.configure(state = "disabled")
                Rester.configure(state = "disabled")
                Rejouer.configure(state = "active")

        elif joueur_valeur == 21:
                rester()
    else: 
        if joueur_valeur>21:
            if jeu_split == "deuxieme_main":
                if plus_de_21 == True and calcul_score(main_joueur) > 21:
                    messagebox.showinfo("Fin de partie","Résultat : \n" + "Première main : c'est perdu \n" + "Deuxième main : c'est perdu")
                    Tirer.configure(state = "disabled")
                    Rester.configure(state = "disabled")
                    Rejouer.configure(state = "active")
                else:
                    rester()
            else:
                if calcul_score(main_joueur) > 21:
                    plus_de_21 = True
                tapis.after(1500, main2_split)
    
    Doubler.configure(state = "disabled")
    Split.configure(state = "disabled")
        


def rester ():
    global paquet,banque_valeur,carte_image_en_jeu_banque,place_carte_banque,Score_banque,benefice,premiere_main
    if jeu_split != True:
        while banque_valeur<17:
            
            paquet_vide()

            main_banque.append(paquet.pop())
            carte_image = ImageTk.PhotoImage(cartes.pop())
            carte_image_en_jeu_banque.append(carte_image)

            banque_valeur = calcul_score(main_banque)
        
        if etat_affich_valeur == True:
                Score_banque.config (text =  "Score : " + str(banque_valeur))
            

        for i in range (len(carte_image_en_jeu_banque)):
            tapis.create_image(300+place_carte_banque,200,image = carte_image_en_jeu_banque[i], tags = "carte")
            place_carte_banque+=71

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
        
        Tirer.configure(state = "disabled")
        Rester.configure(state = "disabled")
        Doubler.configure(state = "disabled")
        Split.configure(state = "disabled")
        Rejouer.configure(state = "active")
    
    else: 
        main2_split()

    
    
    
        
def doubler():
    global cash, mise
    if cash < mise:
        cash_vide()
    else:
        cash -= mise
        mise *= 2
        Cash.config(text = "Cash : " + str(cash))
        Mise.config(text = "Mise : " + str(mise))
        tirer()
        if joueur_valeur <= 21:
            rester()

def split():
    global place_carte_joueur,carte_image_en_jeu_joueur,carte_image_en_jeu_joueur2,carte, main_joueur,main_joueur2, jeu_split, mise,cash
    if cash < mise:
        cash_vide()
    
    else:
        carte_image_en_jeu_joueur2 = []
        main_joueur2 =[]
        place_carte_joueur = 0
        main_joueur2.append(main_joueur.pop())
        carte_image_en_jeu_joueur2.append(carte_image_en_jeu_joueur.pop())

        jeu_split = True

        tapis.delete("split")
        
        for i in range (len(carte_image_en_jeu_joueur)):
            tapis.create_image(300+place_carte_joueur,545,image = carte_image_en_jeu_joueur[i], tags = "carte")
            place_carte_joueur+=71
        if etat_affich_valeur == True:
                Score_joueur.config (text = "Score : " + str(calcul_score(main_joueur)))
                
        
        cash -= mise
        mise *= 2
        Cash.config(text = "Cash : " + str(cash))
        Mise.config(text = "Mise 1 : " + str(mise//2)+ "\n" + "\n" + "Mise 2 : " + str(mise//2))

        Doubler.configure(state = "disabled")
        
    
        
def main2_split():
    global main_joueur,main_joueur2,carte_image_en_jeu_joueur,carte_image_en_jeu_joueur2,place_carte_joueur,jeu_split,premiere_main
    premiere_main = calcul_score(main_joueur)
    main_joueur = main_joueur2.copy()
    carte_image_en_jeu_joueur = carte_image_en_jeu_joueur2.copy()
    tapis.delete("split")
    tapis.create_image(300,545,image = carte_image_en_jeu_joueur2[0], tags = "carte")
    place_carte_joueur = 71
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

    if etat_affich_valeur == True:
            Score_joueur.config (text = "Score : " + str(calcul_score(main_joueur)))
            Score_banque.config (text = "Score : " + str(calcul_score(main_banque)))
            
    Tirer.configure(state = "disabled")
    Rester.configure(state = "disabled")
    Distribuer.configure(state = "disabled")
    Rejouer.configure(state = "disabled")
    Split.configure(state = "disabled")
    Doubler.configure(state = "disabled")
    Jeton.configure(state = "active")



def mise_de_10():
    global cash,mise
    
    if cash <= 0:
        cash_vide()
    else:
        mise += 10
        cash -= 10
        Cash.config(text = "Cash : " + str(cash))
        Mise.config(text = "Mise : " + str(mise))
        Distribuer.configure(state = "active")


etat_affich_valeur = False         

def affich_valeur():
    global etat_affich_valeur
    if valeur.get() == 1:
        etat_affich_valeur = True
        Score_banque.config(text = "Score : " + str(calcul_score(main_banque)))
        Score_joueur.config(text = "Score : " + str(calcul_score(main_joueur)))
    else:
        etat_affich_valeur = False
        Score_banque.config(text = "")
        Score_joueur.config(text = "")

def quitter_jeu():
    racine.destroy()

def aide_jeu():
     messagebox.showinfo("Comment jouer ?" , "Différentes étapes à suivre")

def paquet_vide():
    global paquet,cartes
    if len(paquet) < 1:
        messagebox.showwarning("Attention","Il n'y a plus de cartes dans le paquet, un nouveau paquet est mis en jeu.")
        shuffle(cartes_et_images) 
        paquet,cartes = list(zip(*cartes_et_images))  
        paquet = list(paquet)
        cartes = list(cartes)

def cash_vide():
    global cash
    reponse = messagebox.askyesno("Choix","Vous n'avez plus d'argent ou pas assez, voulez-vous rajouter 500 ? \n(Si non, le jeu se fermera)")
    if reponse:
        cash += 500
        Cash.config(text = "Cash : " + str(cash))
    else:
        racine.destroy()


couleur_fond = "#235A4E"
couleur_bordure = "black"
couleur_bouton = "white"

racine = Tk()
racine.title("Blackjack")
tapis = Canvas(racine,bg = couleur_fond, height = 800, width = 900, highlightbackground=couleur_bordure, highlightthickness = 6, relief="ridge")
tapis.grid()

carte_1 = ImageTk.PhotoImage(carte_cachée)
tapis.create_image(110,165,image = carte_1)
tapis.create_image(107,162,image = carte_1)
tapis.create_image(104,159,image = carte_1)

Tirer = Button(tapis,text="Tirer", bg = couleur_bouton,font=("Arial", 17), activebackground = couleur_bouton,command = tirer)
tapis.create_window(90, 775, window=Tirer, width = 150, height = 40)

Rester = Button(tapis, text="Rester",bg = couleur_bouton,font=("Arial", 17), activebackground = couleur_bouton, command = rester)
tapis.create_window(250, 775, width = 150, height = 40,window=Rester)

Distribuer = Button(tapis, text="Distribuer",bg = couleur_bouton,font=("Arial", 17), activebackground = couleur_bouton, command = distribuer)
tapis.create_window(410, 775,width = 150, height = 40, window=Distribuer)

Rejouer = Button(tapis, text = "Rejouer",bg = couleur_bouton,font=("Arial", 17), activebackground = couleur_bouton, command = rejouer )
tapis.create_window(570,775,width = 150, height = 40,window = Rejouer, tags = "Rejouer_bouton")

Doubler = Button(tapis,text = "Doubler",bg = couleur_bouton,font=("Arial", 17), activebackground = couleur_bouton,command = doubler)
tapis.create_window(90,335, width = 150, height = 40,window = Doubler)

Split = Button(tapis, text = "Split",bg = couleur_bouton,font=("Arial", 17), activebackground = couleur_bouton,command = split)
tapis.create_window(90,495,width = 150, height = 40, window = Split)

jeton = PhotoImage(file="jeton.png")
Jeton = Button(tapis, image = jeton, command = mise_de_10)
Jeton.configure(bg = couleur_fond,relief = "flat", activebackground= couleur_fond,borderwidth=0)
tapis.create_window(85,420, window = Jeton)

tapis.create_rectangle(228,88,866,312, width = 5, outline = couleur_bordure)
tapis.create_rectangle(228,433,866,657, width = 5, outline = couleur_bordure)

valeur = IntVar()
valeur_ou_non = Checkbutton(tapis, font=("Arial", 13),bg = couleur_fond,activebackground = couleur_fond , text = "Afficher la valeur des mains", variable = valeur, command = affich_valeur)
tapis.create_window(780,780, window  = valeur_ou_non)

Score_banque = Label(tapis, bg = couleur_fond, text = "",font =("Arial",17))
tapis.create_window(810,69, window = Score_banque)

Score_joueur = Label(tapis, bg = couleur_fond, text = "",font =("Arial",17))
Score_joueur_label = tapis.create_window(810,414, window = Score_joueur)

Cash = Label(tapis,bg = couleur_fond, text = "Cash : " + str(cash),font =("Arial",17) )
tapis.create_window(85,575, window = Cash)

Mise = Label(tapis,bg = couleur_fond, text = "Mise : " + str(mise),font =("Arial",17) )
tapis.create_window(85,650, window = Mise)

Joueur = Label(tapis, text = "Joueur", bg = couleur_fond,font =("Arial",17))
tapis.create_window(547,414, window = Joueur)

Banque = Label(tapis, text = "Banque", bg = couleur_fond,font =("Arial",17))
tapis.create_window(547,69, window = Banque)

interrogation  = PhotoImage(file = "interrogation.png")
Aide = Button(tapis, image = interrogation, bg = "black", activebackground = "black" , command = aide_jeu)
tapis.create_window(895,19, window = Aide)

quitter  = PhotoImage(file = "quitter.png")
Aide = Button(tapis, image = quitter, bg = "black", activebackground = "black", command = quitter_jeu)
tapis.create_window(18,19, window = Aide)

Tirer.configure(state = "disabled")
Rester.configure(state = "disabled")
Distribuer.configure(state = "disabled")
Rejouer.configure(state = "disabled")
Split.configure(state = "disabled")
Doubler.configure(state = "disabled")

racine.mainloop()

