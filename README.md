# BlackJack : 
Quentin BEAUREZ et Rémi ANDONISSAMY L1 MIASHS TD 01 [github](https://github.com/uvsq22204386/Black-Jack)
                                                                                                                    
Le black jack est un jeu de cartes au casino, ici réalisé avec python à l'aide de l'interface graphique tkinter.


## Règles du jeu

[Règles](https://www.regles-de-jeux.com/regle-du-black-jack/)


## Comment jouer ?

Télécharger tous les documents du github et bien ouvrir le dossier dans votre éditeur de code pour qu'il puisse trouver les images, sinon changer le chemin des images.

Différents boutons permettent de réaliser les différentes actions d'un jeu de blackjack.
L'ordre d'utilisation des boutons est important : vous ne pouvez pas tirer une carte sans avoir miser ou distribuer par exemple. 

Quel est l'ordre ?

- Miser (en cliquant sur l'image de jeton), chaque appui sur le bouton ajoute 10 à votre mise totale
- Distribuer 
- Selon votre choix : tirer, rester ou doubler, split si vous avez une paire
- Si vous avez tiré, vous pouvez encore tirer ou bien rester si vous n'avez pas dépassé 21
- Rester met fin à votre partie 
- Rejouer permet alors de faire les paiements en fonction du gagnant et de lancer une nouvelle partie


## Informations utiles
 - Lorsque le programme est lancé, un paquet mélangé est mis en jeu, si pendant que vous jouez, vous utilisez toutes les cartes du paquet alors un nouveau paquet va être mis en jeu
 - Lorsque vous essayez de miser plus que ce que vous avez, alors vous aurez la possibilité, soit de récupérer 500 crédits ou bien de fermer le jeu à l'aide un message
 qui vous sera affiché
 - Lors de l'utilisation du split, votre paire est divisée en 2 mains différentes et votre mise doublée, vous jouez d'abord votre première main puis lorsque vous avez 
 appuyé sur rester ou dépasser 21 avec cette première main vous passez à la deuxième main, et enfin le bilan des deux mains
 - Lors de l'utilisation de doubler, votre mise est doublée et vous tirez une seule carte entraînant la fin de la partie 

Boutons bonus : afficher la valeur des mains, quitter, aide.

## Sources

- [icones8](https://icones8.fr/) : icones quitter et aide
- [flaticon](https://www.flaticon.com/fr/) : icone jeton
