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
   
    paquet_vide() # permet de lancer une fonction qui vérifie si le paquet n'est pas vide

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
    
    # Affichage des cartes sur le tapis :
    for i in range (len(carte_image_en_jeu_joueur)): 
        # Boucle pour afficher chaque image des cartes du joueur en jeu
        tapis.create_image(300+place_carte_joueur,545,image = carte_image_en_jeu_joueur[i], tags = ("carte", "split"))
        place_carte_joueur+=71 # cette variable permet de décaler les cartes 
    
    for i in range (len(carte_image_en_jeu_banque)):
        tapis.create_image(300+place_carte_banque,200,image = carte_image_en_jeu_banque[i] , tags = "carte")
    
    carte_image_cachée = ImageTk.PhotoImage(carte_cachée)
    tapis.create_image(300 + 71,200,image = carte_image_cachée, tag = "carte") # affiche une carte cachée correspondant à la deuxième carte de la banque
    
    # Permet d'afficher les scores si le bouton a été coché :
    if etat_affich_valeur == True:
        Score_banque.config (text =  "Score : " + str(banque_valeur))
        Score_joueur.config (text = "Score : " + str(joueur_valeur))
    
    # Si le joueur a 21 à la distribution : blackjack donc la partie est finie et il gagne sa mise plus 1.5 fois sa mise :
    if calcul_score(main_joueur) == 21:
        messagebox.showinfo("Fin de partie","Résultat : gagné") # Message pour indiquer qu'il a gagné
        benefice = 2*mise + mise//2
        
        # Permet de désactiver les boutons qui ne peuvent pas être utilisés et activer les autres :
        Tirer.configure(state = "disabled")
        Rester.configure(state = "disabled")
        Rejouer.configure(state = "active")

    Jeton.configure(state = "disabled")
    Distribuer.configure(state = "disabled")
    Tirer.configure(state = "active")
    Rester.configure(state = "active")
    Doubler.configure(state = "active")

    # Permet d'activer le bouton split si le joueur a une paire :
    if main_joueur[0][0] == main_joueur[1][0]:
         Split.configure(state = "active")
    

def tirer ():
    '''Cette fonction permet au joueur de tirer une carte s'il le veut'''
    global paquet,main_joueur, joueur_valeur,carte_image,place_carte_joueur,carte_image_en_jeu_joueur,Score_joueur, plus_de_21
    
    paquet_vide()

    # Distribution d'une carte au joueur :
    main_joueur.append(paquet.pop())
    joueur_valeur = calcul_score(main_joueur)
        
    carte_image = ImageTk.PhotoImage(cartes.pop())
    carte_image_en_jeu_joueur.append(carte_image)
    
    # Permet d'afficher les cartes du joueur :
    for i in range (len(carte_image_en_jeu_joueur)):
        tapis.create_image(300+place_carte_joueur,545,image = carte_image_en_jeu_joueur[i], tags= ("carte","split"))
    place_carte_joueur += 71
    
    # Permet d'actualiser le score du joueur si l'option est activée
    if etat_affich_valeur == True:
                    Score_joueur.config (text = "Score : " + str(joueur_valeur))

    # Si le joueur n'a pas active split
    if jeu_split == False : 
        # Si le joueur dépasse 21 en tirant : fin de partie
        if joueur_valeur > 21:
                messagebox.showinfo("Fin de partie","Résultat : perdu")
                Tirer.configure(state = "disabled")
                Rester.configure(state = "disabled")
                Rejouer.configure(state = "active")
        # Si le joueur à 21, le jeu active rester directement car meilleur score
        elif joueur_valeur == 21:
                rester()
    # Si le joueur a activé split
    else: 
        # Vérifie si la main est au dessus de 21 :
        if joueur_valeur>21:
            # Vérifie si on est sur la deuxième main du split :
            if jeu_split == "deuxieme_main":
                # Vérifie si la première main est au-dessus de 21 et la dexuième aussi :
                if plus_de_21 == True and calcul_score(main_joueur) > 21:
                    messagebox.showinfo("Fin de partie","Résultat : \n" + "Première main : c'est perdu \n" + "Deuxième main : c'est perdu")
                    
                    # Permet de désactiver les boutons qui ne peuvent pas être utilisés et activer les autres :
                    Tirer.configure(state = "disabled")
                    Rester.configure(state = "disabled")
                    Rejouer.configure(state = "active")

                # Si la deuxième main n'est pas au dessus de 21, rester pour que la banque tire ses cartes et affiche le résultat :
                else:
                    rester()
            # Si le jeu n'est pas à la deuxième main 
            else:
                # Vérifie si la première main est à plus de 21 :
                if calcul_score(main_joueur) > 21:
                    plus_de_21 = True # Indique que la première main est à 21 pour la suite de la partie
                tapis.after(1500, main2_split) # Attend 1.5sc pour que le joueur voit qu'il a dépassé 21 avec sa première main puis lance la fonction pour passer à la deuxième main
    
    # Permet de désactiver les boutons qui ne peuvent pas être utilisés et activer les autres :
    Doubler.configure(state = "disabled")
    Split.configure(state = "disabled")
        


def rester ():
    '''Cette fonction permet au joueur de rester s'il le veut, cela entrainera le tirage de la banque et la fin de partie avec la comparaison des scores entre la banque et le joueur'''
    global paquet,banque_valeur,carte_image_en_jeu_banque,place_carte_banque,Score_banque,benefice,premiere_main
    # Si le joueur n'a pas split ou n'est pas à la deuxième main du split :
    if jeu_split != True:
        # La banque tire jusqu'à avoir 17 ou plus :
        while banque_valeur<17:
            
            paquet_vide()

            # La banque tire une carte :
            main_banque.append(paquet.pop())
            carte_image = ImageTk.PhotoImage(cartes.pop())
            carte_image_en_jeu_banque.append(carte_image)

            # Calcul de la valeur de la main de la banque :
            banque_valeur = calcul_score(main_banque)
        
        # Permet d'actualiser le score de la banque si l'option est activée :
        if etat_affich_valeur == True:
                Score_banque.config (text =  "Score : " + str(banque_valeur))
            
        # Permet d'afficher les cartes de la banque :
        for i in range (len(carte_image_en_jeu_banque)):
            tapis.create_image(300+place_carte_banque,200,image = carte_image_en_jeu_banque[i], tags = "carte")
            place_carte_banque+=71 # Décalage pour la prochaine carte

        # Si la première main a une valeur à 0 : le joueur n'a pas split
        if premiere_main == 0: 
            # Affichage le résultat de la partie et définit le bénéfice:
            if banque_valeur > 21 or joueur_valeur>banque_valeur:
                messagebox.showinfo("Fin de partie","Résultat : gagné")
                benefice = 2*mise
                
            elif banque_valeur>joueur_valeur:
                messagebox.showinfo("Fin de partie","Résultat : perdu")
                
            else: 
                messagebox.showinfo("Fin de partie","Résultat : égalité")
                benefice = mise

        # Si la première main a une valeur différente à 0 : le jouer a split 
        else:
            # Bilan de la première main : 
            if premiere_main > 21 or (banque_valeur > premiere_main and banque_valeur <= 21):
                resultat_premiere_main = "perdu"
            elif premiere_main == banque_valeur:
                resultat_premiere_main = "egalite"
            elif premiere_main > banque_valeur or banque_valeur > 21:
                resultat_premiere_main = "gagne"
            
            # Bilan de la dexuième main : 
            if joueur_valeur > 21 or (banque_valeur > joueur_valeur and banque_valeur <= 21):
                resultat_deuxieme_main = "perdu"
            elif joueur_valeur == banque_valeur:
                resultat_deuxieme_main = "egalite"
            elif joueur_valeur > banque_valeur or banque_valeur > 21:
                resultat_deuxieme_main = "gagne"

            # Affichage le résultat de la partie et définit le bénéfice en fonction du résultat des deux mains :
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
        
        # Permet de désactiver les boutons qui ne peuvent pas être utilisés et activer les autres :
        Tirer.configure(state = "disabled")
        Rester.configure(state = "disabled")
        Doubler.configure(state = "disabled")
        Split.configure(state = "disabled")
        Rejouer.configure(state = "active")
    
    else: 
        # Permet de passer à la deuxième main :
        main2_split()

    
    
    
        
def doubler():
    "Cette fonction permet au joueur de doubler sa mise et de tirer une seule carte ce qui entrainera la fin de partie avec le tirage de la banque et la comparaison"
    global cash, mise

    # Vérification si le joueur a assez pour doubler sa mise : 
    if cash < mise:
        cash_vide()
    else:
        cash -= mise # Double la mise en enlevant la mise de bas au cash
        mise *= 2 # Double la mise

        # Actualisation de la mise et du cash affichés :
        Cash.config(text = "Cash : " + str(cash))
        Mise.config(text = "Mise : " + str(mise))
        tirer() # Tire l'unique carte
        if joueur_valeur <= 21: # Si le joueur a moins de 21 ou 21, il active la fonction rester directement pour finir la partie (car à plus de 21 la fonction tirer finit directement la partie)
            rester()

def split():
    '''Cette fonction permet au joueur de "split" sa paire s'il en a une'''
    global place_carte_joueur,carte_image_en_jeu_joueur,carte_image_en_jeu_joueur2,carte, main_joueur,main_joueur2, jeu_split, mise,cash
    # Vérification si le joueur a assez pour doubler sa mise :
    if cash < mise:
        cash_vide()
    
    else:
        # Définition de nouvelles variables pour contenir la deuxième main :
        carte_image_en_jeu_joueur2 = []
        main_joueur2 =[]
        
        place_carte_joueur = 0
        
        # Ajoute à la deuxième main et enlève à la première une des 2 cartes de la paire :
        main_joueur2.append(main_joueur.pop())
        carte_image_en_jeu_joueur2.append(carte_image_en_jeu_joueur.pop())

        # Définit que le joueur a utilisé split pour pouvoir faire des actions différentes de celles classique dans tirer et rester :
        jeu_split = True

        # Supprime la deuxième carte de l'affichage :
        tapis.delete("split")
        
        # Affiche les cartes de la première main :
        for i in range (len(carte_image_en_jeu_joueur)):
            tapis.create_image(300+place_carte_joueur,545,image = carte_image_en_jeu_joueur[i], tags = "carte")
            place_carte_joueur+=71
        
        # Permet d'afficher le score de la première main si l'option est activée :
        if etat_affich_valeur == True:
            Score_joueur.config (text = "Score : " + str(calcul_score(main_joueur)))
                
        # Double la mise :
        cash -= mise
        mise *= 2
        
        # Actualise l'affichage de la mise et cash :
        Cash.config(text = "Cash : " + str(cash))
        Mise.config(text = "Mise 1 : " + str(mise//2)+ "\n" + "\n" + "Mise 2 : " + str(mise//2))

        Doubler.configure(state = "disabled")
        
    
        
def main2_split():
    '''Cette fonction permet de changer la main du joueur utilisée en cours par la deuxième, si le joueur a activé la fonction split '''
    global main_joueur,main_joueur2,carte_image_en_jeu_joueur,carte_image_en_jeu_joueur2,place_carte_joueur,jeu_split,premiere_main
    
    premiere_main = calcul_score(main_joueur) # Garde en mémoire le score de la première main
    
    # Remplace la première main par la deuxième main :
    main_joueur = main_joueur2.copy() 
    carte_image_en_jeu_joueur = carte_image_en_jeu_joueur2.copy()
    
    tapis.delete("split") # Supprime l'affichage de la première main 

    tapis.create_image(300,545,image = carte_image_en_jeu_joueur2[0], tags = "carte") # Affiche la deuxième carte de la paire
    place_carte_joueur = 71

    jeu_split = "deuxieme_main" # Variable pour savoir qu'on est passé à la deuxième main

    # Permet d'afficher le score de la deuxième main du joueur si l'option est activée
    if etat_affich_valeur == True:
            Score_joueur.config (text = "Score : " + str(calcul_score(main_joueur)))

def calcul_score(main):
    ''' Cette fonction permet de calculer la valeur d'une main passée en paramètre'''
    score = 0
    As = 0
    # Calcul du score de chaque carte de la main et additionne ces scores dans score
    for card in main:
        # Chaque élément de la liste correspond à un couple contenant un nombre ou une tête et une couleur : l'élément d'indice 0 corresspond au nombre ou à la tête
        if card[0] == "Valet" or card[0] == "Reine" or card [0] == "Roi": # Chaque tête a pour valeur 10
            score +=10
        elif card[0] == "As":
            score += 11 # au départ l'as est comptabilisé comme 11
            As += 1 # Comptage du nombre d'as 
        else:
            score+= int(card[0]) # si c'est un nombre alors le score correspond à ce nombre
    while As>0 and score>21:  # tant qu'il y a des as et un score supérieur à 21 : passage de la valeur de l'as à 1 donc -10
        As -=1
        score -=10
    return score

def rejouer():
    ''' Cette fonction permet de récupérer l'argent que la banque nous doit ou de donner notre mise à la banque ainsi que de relancer une partie'''
    global place_carte_banque,place_carte_joueur,carte_image_en_jeu_banque,carte_image_en_jeu_joueur, Score_banque, main_joueur,main_banque,mise,cash,benefice

    tapis.delete("carte") # supression de toutes les cartes (tous les widgets qui avaient le tag "carte")
    
    # réinitialisation de toutes les données propre à chaque partie
    main_joueur = []
    main_banque = []

    place_carte_joueur = 0
    place_carte_banque = 0
    
    carte_image_en_jeu_joueur= []
    carte_image_en_jeu_banque = []

    mise = 0
    cash += benefice # ajout du bénéfice de la partie au cash total
    benefice = 0

    # Affichage remis à 0 :
    Mise.config(text = "Mise : 0")
    Cash.config (text = "Cash : " + str(cash + benefice))
    
    # Permet d'actualiser le score de la banque et le joueur à 0 si l'option est activée :
    if etat_affich_valeur == True:
            Score_joueur.config (text = "Score : " + str(calcul_score(main_joueur)))
            Score_banque.config (text = "Score : " + str(calcul_score(main_banque)))
    
    # Permet de désactiver les boutons qui ne peuvent pas être utilisés et activer les autres :
    Tirer.configure(state = "disabled")
    Rester.configure(state = "disabled")
    Distribuer.configure(state = "disabled")
    Rejouer.configure(state = "disabled")
    Split.configure(state = "disabled")
    Doubler.configure(state = "disabled")
    Jeton.configure(state = "active")



def mise_de_10():
    ''' Cette fonction permet de miser 10'''
    global cash,mise
    
    # Vérification si le joueur a assez pour miser :
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
    '''Cette fonction permet d'afficher ou non la valeur des mains en jeu'''
    global etat_affich_valeur
    if valeur.get() == 1: # Vérifie si le bouton est coché ou non
        etat_affich_valeur = True # Permet de vérifier dans les différentes fonctions si le bouton est coché pour savoir s'il faut actualiser les valeurs de score
        Score_banque.config(text = "Score : " + str(calcul_score(main_banque)))
        Score_joueur.config(text = "Score : " + str(calcul_score(main_joueur)))
    else:
        etat_affich_valeur = False
        Score_banque.config(text = "")
        Score_joueur.config(text = "")

def quitter_jeu():
    '''Cette fonction permet de fermer la fenêtre de jeu'''
    racine.destroy()

def aide_jeu():
    '''Cette fonction permet d'ouvir une aide qui explique comment jouer sur ce jeu de blackjack'''
    messagebox.showinfo("Comment jouer ?" , """Pour jouer, vous devez appuyer sur les différents boutons, cependant il y a un ordre à respecter :
    - Miser (en cliquant sur l'image de jeton), chaque appui sur le bouton ajoute 10 à votre mise totale
    - Distribuer
    - Selon votre choix : tirer, rester ou doubler, split si vous avez une paire
    - Si vous avez tiré, vous pouvez encore tirer ou bien rester si vous n'avez pas dépassé 21
    - Rester met fin à votre partie
    - Rejouer permet alors de faire les paiements en fonction du gagnant et de lancer une nouvelle partie
    
Pour plus d'informations veuillez-vous réferrer au README.md, notamment pour comment utiliser le split et les règles du jeu."""
    )

def paquet_vide():
    '''Cette fonction vérifie si le paquet de cartes est vide'''
    global paquet,cartes
    if len(paquet) < 1: # Vérification si le paquet est vide
        messagebox.showwarning("Attention","Il n'y a plus de cartes dans le paquet, un nouveau paquet est mis en jeu.")
        shuffle(cartes_et_images) # Remélange l'association de carte et image
        paquet,cartes = list(zip(*cartes_et_images))  # Recrée un paquet avec les images qui y sont associées
        paquet = list(paquet)
        cartes = list(cartes)

def cash_vide():
    '''Cette fonction demande au joueur s'il veut récupérer 500 ou bien fermer le jeu '''
    global cash
    reponse = messagebox.askyesno("Choix","Vous n'avez plus d'argent ou pas assez, voulez-vous rajouter 500 ? \n(Si non, le jeu se fermera)")
    if reponse:
        cash += 500
        Cash.config(text = "Cash : " + str(cash))
    else:
        racine.destroy()

# Définition des couleurs utilisées :
couleur_fond = "#235A4E"
couleur_bordure = "black"
couleur_bouton = "white"

# Définition de la fenêtre principale :
racine = Tk()
racine.title("Blackjack")

# Défintion du canva correspondant au tapis :
tapis = Canvas(racine,bg = couleur_fond, height = 800, width = 900, highlightbackground=couleur_bordure, highlightthickness = 6, relief="ridge")
tapis.grid()

# Affichage de 3 images de cartes cachées pour créer une impression de paquet de carte :
carte_1 = ImageTk.PhotoImage(carte_cachée)
tapis.create_image(110,165,image = carte_1)
tapis.create_image(107,162,image = carte_1)
tapis.create_image(104,159,image = carte_1)

# Création des différents boutons du jeu :
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
Jeton = Button(tapis, image = jeton, command = mise_de_10,bg = couleur_fond,relief = "flat", activebackground= couleur_fond,borderwidth=0)
tapis.create_window(85,420, window = Jeton)

interrogation  = PhotoImage(file = "interrogation.png")
Aide = Button(tapis, image = interrogation, bg = "black", activebackground = "black" , borderwidth = 0, command = aide_jeu)
tapis.create_window(895,19, window = Aide)

quitter  = PhotoImage(file = "quitter.png")
Aide = Button(tapis, image = quitter, bg = "black", activebackground = "black", borderwidth = 0, command = quitter_jeu)
tapis.create_window(18,19, window = Aide)

# Création des 2 rectangles où les cartes s'afficheront 
tapis.create_rectangle(228,88,866,312, width = 5, outline = couleur_bordure)
tapis.create_rectangle(228,433,866,657, width = 5, outline = couleur_bordure)

# Création du bouton à cocher
valeur = IntVar()
valeur_ou_non = Checkbutton(tapis, font=("Arial", 13),bg = couleur_fond,activebackground = couleur_fond , text = "Afficher la valeur des mains", variable = valeur, command = affich_valeur)
tapis.create_window(780,780, window  = valeur_ou_non)

# Création des différents labels affichés : 
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

# Permet de désactiver les boutons qui ne peuvent pas être utilisés et activer les autres :
Tirer.configure(state = "disabled")
Rester.configure(state = "disabled")
Distribuer.configure(state = "disabled")
Rejouer.configure(state = "disabled")
Split.configure(state = "disabled")
Doubler.configure(state = "disabled")

racine.mainloop()

