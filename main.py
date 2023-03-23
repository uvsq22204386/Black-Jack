from random import*
from tkinter import*
from PIL import Image, ImageTk


couleurs = ["Trèfle","Carreau","Coeur","Pique"]
rangs = ['As','2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valet', 'Reine', 'Roi']
paquet = []

for couleur in couleurs:
    for rang in rangs:
        paquet.append((rang,couleur))

image = Image.open("C:\\Users\\quent\\OneDrive\\Bureau\\BlackJack\\cartes.png")

carte_cachée_taille = (0,0,110,170)
carte_cachée = image.crop(carte_cachée_taille)


carte_largeur = image.width
carte_hauteur = image.height // 53


cartes = []

for i in range(52):

    carte_x = 0
    carte_y = i * carte_hauteur + 170
    carte_box = (carte_x, carte_y, carte_x + carte_largeur, carte_y + carte_hauteur)
    carte = image.crop(carte_box)
    cartes.append(carte)

cartes_et_images = list(zip(paquet,cartes))

shuffle(cartes_et_images)

paquet,cartes = list(zip(*cartes_et_images))

paquet = list(paquet)
cartes = list(cartes)

place_carte_joueur = 0
place_carte_banque = 0
carte_image_en_jeu_joueur= []
carte_image_en_jeu_banque = []

état = ""

def distribuer ():
    global paquet, main_joueur, main_banque,joueur_valeur,banque_valeur,place_carte_joueur,place_carte_banque,carte_image_en_jeu_joueur,carte_image_cachée,Score_banque, Score_joueur
    
    main_joueur = []
    main_banque = []
    
    main_joueur.append(paquet.pop())
    carte_image = ImageTk.PhotoImage(cartes.pop())
    carte_image_en_jeu_joueur.append(carte_image)
    
    main_banque.append(paquet.pop())
    carte_image = ImageTk.PhotoImage(cartes.pop())
    carte_image_en_jeu_banque.append(carte_image)
    
    main_joueur.append(paquet.pop())
    carte_image = ImageTk.PhotoImage(cartes.pop())
    carte_image_en_jeu_joueur.append(carte_image)
    
    joueur_valeur = calcul_score(main_joueur)
    banque_valeur = calcul_score(main_banque)
    

    for i in range (len(carte_image_en_jeu_joueur)):
        tapis.create_image(300+place_carte_joueur,600,image = carte_image_en_jeu_joueur[i], tags = "carte")
        place_carte_joueur+=55 
    
    for i in range (len(carte_image_en_jeu_banque)):
        tapis.create_image(300+place_carte_banque,300,image = carte_image_en_jeu_banque[i] , tag = "carte")
    
    carte_image_cachée = ImageTk.PhotoImage(carte_cachée)
    tapis.create_image(300 + 55,300,image = carte_image_cachée, tag = "carte")
    
    if etat_affich_valeur == True:
        Score_banque.config (text =  "Score : " + str(banque_valeur))
        Score_joueur.config (text = "Score : " + str(joueur_valeur))
    

def tirer ():
    global paquet,main_joueur, joueur_valeur,carte_image,place_carte_joueur,carte_image_en_jeu_joueur,Score_joueur
    
    main_joueur.append(paquet.pop())
    joueur_valeur = calcul_score(main_joueur)
    
    carte_image = ImageTk.PhotoImage(cartes.pop())
    carte_image_en_jeu_joueur.append(carte_image)
    
    for i in range (len(carte_image_en_jeu_joueur)):
        tapis.create_image(300+place_carte_joueur,600,image = carte_image_en_jeu_joueur[i], tags= "carte")
    place_carte_joueur += 55
    if joueur_valeur > 21:
        résultat.config(text = "Résultat : perdu")
    elif joueur_valeur == 21:
        rester()
    
    if etat_affich_valeur == True:
        Score_joueur.config (text = "Score : " + str(joueur_valeur))

    
def rester ():
    global paquet,banque_valeur,carte_image_en_jeu_banque,place_carte_banque,Score_banque
    while banque_valeur<17:
        main_banque.append(paquet.pop())
        carte_image = ImageTk.PhotoImage(cartes.pop())
        carte_image_en_jeu_banque.append(carte_image)

        banque_valeur = calcul_score(main_banque)
        

    for i in range (len(carte_image_en_jeu_banque)):
        tapis.create_image(300+place_carte_banque,300,image = carte_image_en_jeu_banque[i], tags = "carte")
        place_carte_banque+=55

    if banque_valeur > 21 or joueur_valeur>banque_valeur:
        résultat.config(text = "Résultat : gagné")
    elif banque_valeur>joueur_valeur:
        résultat.config(text = "Résultat : perdu")
    else: 
        résultat.config(text = "Résultat : égalité")

    if etat_affich_valeur == True:
        Score_banque.config (text =  "Score : " + str(banque_valeur))
        
    

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
    global place_carte_banque,place_carte_joueur,carte_image_en_jeu_banque,carte_image_en_jeu_joueur, Score_banque

    tapis.delete("carte")
    résultat.config(text = "Résultat :")
    Score_banque.config(text ="")
    Score_joueur.config(text = "")
    
    place_carte_joueur = 0
    place_carte_banque = 0
    
    carte_image_en_jeu_joueur= []
    carte_image_en_jeu_banque = []
          

etat_affich_valeur = False         

def affich_valeur():
    global etat_affich_valeur, valeur_banque
    if valeur.get() == 1:
        etat_affich_valeur = True
        Score_banque.config(text = "Score : " + str(calcul_score(main_banque)))
        Score_joueur.config(text = "Score = " + str(calcul_score(main_joueur)))
    else:
        etat_affich_valeur = False
        Score_banque.config(text = "")
        Score_joueur.config(text = "")

racine = Tk()

tapis = Canvas(bg = "#{:02x}{:02x}{:02x}".format(35, 90, 78), height = 800, width = 900, highlightbackground="#{:02x}{:02x}{:02x}".format(156, 28, 30), highlightthickness=3, relief="ridge")

Tirer = Button(tapis, text="Tirer", command = tirer)
Rester = Button(tapis, text="Rester", command = rester)
Distribuer = Button(tapis, text="Distribuer", command = distribuer)
Rejouer = Button(tapis, text = "Rejouer", command = rejouer)
résultat = Label(tapis, text = "Résultat :")

jeton = PhotoImage(file="C:\\Users\\quent\\OneDrive\\Bureau\\BlackJack\\jeton1.png")
Jeton = Button(tapis, image = jeton)
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

tapis.create_window(200, 750, window=Tirer)
tapis.create_window(400, 780, window=Rester)
tapis.create_window(600, 780, window=Distribuer)
tapis.create_window(600,400, window = résultat)
tapis.create_window(600,700,window = Rejouer)

tapis.grid()


racine.mainloop()


