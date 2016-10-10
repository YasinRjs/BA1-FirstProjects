################################################
#                                              #
#           Projet1 : Le Bonneteau             #
#         INFO-F-101 : Programmation           #
#           Matricule : 000396506              #
#               Yasin Arslan                   #
#                                              #
################################################

__author__="Yasin Arslan (Matricule : 000396506)"
__date__="20 Octobre 2014"

"""
   Ce programme simule le jeu de Bonneteau.
   Le joueur doit trouver la position du jeton parmis les 3 gobelets.
   Utilisateur dit "intelligent".
"""

from random import randint

#Impression de Bienvenue

print("###\nBienvenue dans le jeu de Bonneteau.")
print("Vous devrez choisir l'un des 3 gobelets.")
print("Gauche (G) , Milieu (M) , Droite (D).")
print("Si votre gobelet cache le jeton, c'est gagné !\n###")

################### Initiation de variable ####################
G=0
M=1
D=2
mise=0
tour=1
STOP=-1   #CONSTANTE pour arreter le jeu.

#####################     Debut du jeu    ############################


#Montant de depart de l'utilisateur.
print("Votre somme d'argent est de : ",end="")
total = float(input())     #Float pour prendre les centimes en compte.
total_save=total           #Sauvegarde montant de départ.

#Debut du jeu. Condition pour arrêter le jeu: soit plus d'argent, soit input STOP.
while mise!=STOP and total>0:
    
  #Placement du jeton entre gobelet Gauche(0),Milieu(1),Droite(2).
  jeton=randint(0,2)

  #Affichage du tour et demande de mise.
  print("### Tour ",tour)
  print("Le montant que vous misez ce tour (tapez ",STOP," pour arrêter) : ",end="")
  mise = float(input())
  tour+=1  #Incremente tour pour preparer le tour suivant.
  
  #Mise superieur a l'argent poseder, mise nulle ou negatif.
  #Demande a nouveau. Utilisateur semi-intelligent.
  while (mise>total) or (mise<=0) and mise!=STOP:
    if mise>total:
      print("Vous n'avez pas autant d'argent !")
    else:
      print("Votre mise est nulle ou negatif.")
    print("Le montant que vous misez ce tour (tapez ",STOP," pour arrêter) : ",end="")
    mise = float(input())
  
  #Mise correcte.
  if mise!=STOP:
    print("Veuillez choisir votre gobelet entre G, M et D : ",end="")
    choix = input()
    choix = choix.upper()
    while choix!="G" and choix!="M" and choix!="D":
      print("Ce gobelet n'existe pas, Gauche(G);Milieu(M);Droite(D) : ",end="")
      choix = input()
      choix = choix.upper()
    choix = eval(choix)          #Input d'un str a transformer en int.
    
        
    #Victoire
    if choix==jeton:
      print("Félicitation vous avez gagné !\nVotre mise de ",mise, " est doublé et s'ajoute a votre total.")
      total+=(mise*2)
    
    #Defaite
    else:
      print("Perdu ! Vous aurez plus de chance la prochaine fois.")
      total-=mise
      
  print("Il vous reste : ",total,"\n")

#Gain/Perte finale.
gain=total-total_save

print("### Fin du jeu ###\nVous avez ",total,"euro(s) dans votre poche.")

#######################   Fin du jeu   ###########################

#Montant final supérieur a montant depart.
if total>total_save:
  print("Vous avez gagné : ",gain,"euro(s).")

#L'argent final en poche vaut l'argent de base.
elif total==total_save and total_save>0:
  print("Vous n'avez rien gagné et vous n'avez rien perdu.")

#Plus de sous.
elif total<=0:
  print("Vous êtes fauché !")
else:
  print("Vous avez perdu : ",abs(gain),"euro(s)")    #abs(gain) pour ne pas avoir un nombre négatif.
