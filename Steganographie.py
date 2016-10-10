#--- kubrick.pgm ---
#The cake is a lie !
#The cake is a lie !
#The cake is a lie !
#The cake is a lie !

#--- math.pgm ---
#Bien joué l'amis, tu as trouvé le dessin secret ...

################################################
#                                              #
#        Projet 4 : La stéganographie          #
#        INFO-F-101 : Programmation            #
#        Matricule : 000396506                 #
#                                              #
################################################

__author__="Yasin Arslan (Matricule : 000396506)"
__date__="10 November 2014"

"""
   Code permetant de faire de la stéganographie.
   C'est à dire dissimuler une image dans une autre ou encore
   dévoiler une image dissimulé dans une image source.
   Pour l'utilisation il faudra taper les arguments suivants :
   * codage   imageSource.pgm   imageCode.pgm   imageRes.pgm
   * decodage   imageRes.pgm  imageCode.pgm
"""

from sys import argv

#=====================
def info_image(image):
#=====================
  """
  Fonction qui va ouvrir une image et lire les 3 premieres lignes.
  Il renverra le type, la colonne,la ligne et le niveau de gris du fichier."""
  f = open(image)
  PGM = "P2"
  #On nettoie espaces et \n inutile pour les lignes avec strip().
  file_type = f.readline().strip()
  #On affiche directement une erreur si le fichier donné n'est pas un PGM.
  #On force l'erreur pour arrêter directement le programme et ne rien faire
  #d'inutile en plus.
  if file_type != PGM:
    raise TypeError
  
  column,line = f.readline().split()
  max_pixel = f.readline().strip()
  f.close()
  #Retourne tuple (type_fichier,colonne,ligne,max_pixel)
  return (file_type,int(column),int(line),max_pixel)


#========================
def charger_image(image):
#========================
  """
  Fonction qui va charger une image et renvoyer la matrice correspondant
  aux pixels de l'image."""
  f = open(image)
  #On strip() les elements inutile et on split chaque nombres.
  texte = f.read().strip().split()
  #On prends les infos colonne/ligne pour l'utilisation prochaine.
  file_type,column,line,max_pixel = info_image(image)
  liste = []
  matrice = []
  #On commence par le 5 eme element ( indice 4 ).
  #Les 4 premiers sont à la ligne 62.
  texte = texte[4:]
  longueur = len(texte)
  #Tout les elements ( à partir du 4e ) vont être pris.
  for elem in texte:
    liste.append(elem)
    if len(liste) == column:
      matrice.append(liste)
      liste = []
  f.close()
  return matrice

#=========================
def verif_image(source,code):
  """
  Fonction qui vérifie la taille et max_pixel des fichiers.
  Source doit avec 256 niveaux de gris, Code doit en avoir 2."""
  #Prise des infos pour vérifier les caracteristiques. Taille, max_pixel.
  type_source,line_source,column_source,pixel_source = info_image(source)
  type_code,line_code,column_code,pixel_code = info_image(code)
  max_source = "255"
  max_code = "1"
  
  return (line_source == line_code and column_source == column_code \
  and pixel_source == max_source and pixel_code == max_code)

#==========================================
def create_file(source,matrice_source,res):
#==========================================
  """
  Création du nouveau fichier pgm du resultat."""
  
  CODAGE = "codage"
  type_file,column,line,max_pixel = info_image(source)
  #Ouverture du fichier en écriture, si celui-ci n'existe pas on le crée.
  f = open(res,"w")
  f.write("{}\n{} {}\n".format(type_file,str(column),str(line)))
  if argv[1].lower() == CODAGE:
    f.write("{}\n".format(max_pixel))
  else:
    #2 niveaux de gris ( "0" blanc, "1" noir )
    f.write("1\n")
    
  for line in matrice_source:
    for car in line:
      f.write("{} ".format(str(car)))
    f.write("\n")
  
  f.close()

#============================
def encrypt(source,code,res):
#============================
  """
  Fonction qui code une image dans une autre si ceux-ci respectent
  les caractéristiques demandé de la fonction verif_image."""
  #Chargement des matrices code/source
  print("---- Début du codage ----")
  print("Fichier source : {}".format(source))
  print("Fichier code : {}".format(code))
  print("Fichier destination : {}".format(res))
  matrice_source = charger_image(source)
  matrice_code = charger_image(code)
  white = 0
  #Vérification des caracteristiques.
  if verif_image(source,code):

    #On va modifier la matrice source pour avoir des nombres paires aux
    #indices dans lesquels sont caché l'image code donc noir.
    #Et les nombres impaires seront blanc dans le fichier code.
    #Cette matrice sera le nouveau fichier créer.
    line = len(matrice_code)
    column = len(matrice_code[0])
    for i in range(line):
      for j in range(column):
        if int(matrice_code[i][j]) != white and (int(matrice_source[i][j])%2 == 0):
          matrice_source[i][j] = int(matrice_source[i][j]) + 1
        elif int(matrice_code[i][j]) == white and (int(matrice_source[i][j])%2 == 1):
          matrice_source[i][j] = int(matrice_source[i][j]) - 1
        else:
          matrice_source[i][j] = int(matrice_source[i][j])
   
    create_file(source,matrice_source,res)
    print("---- Codage terminé avec succès ! ----")
 
  else:
    print("Les fichiers ne respectent pas les caractéristiques demandé.")

#=======================
def decrypt(source,res):
#=======================
  """
  Fonction qui va retirer l'éventuel message caché derrière l'image
  donné et l'écris dans un nouveau fichier."""

  print("---- Début du décodage ----")
  print("Fichier contenant le message : {}".format(source))
  print("Fichier du message codé : {}".format(res))
  matrice_source = charger_image(source)
  #Création de line et column pour ne pas appeler la fonction len()
  #A chaque tour dans la boucle
  line = len(matrice_source)
  column = len(matrice_source[0])

  #Modification de matrice_source pour ne pas créer une nouvelle matrice.
  #Celle-ci va contenir que des 0 et 1 ( niveau de gris 1 ).
  #Convention de l'énoncé, nombre pair devient blanc,impair devient noir.
  #Cette matrice contiendra le code caché dans la matrice_source de départ.
  for i in range(line):
    for j in range(column):
      if int(matrice_source[i][j])%2 == 0:
        matrice_source[i][j] = 0
      else:
        matrice_source[i][j] = 1

  create_file(source,matrice_source,res)
  print("---- Decodage terminé avec succès ! ----")

def main():
  CODAGE = "codage"
  DECODAGE = "decodage"
  try:
    action = argv[1].lower()
    imageSource = argv[2]
    if action == CODAGE:
      imageCode = argv[3]
      imageRes = argv[4]
      encrypt(imageSource,imageCode,imageRes)
    elif action == DECODAGE:
      imageRes = argv[3]
      decrypt(imageSource,imageRes)
    else:
      print("Action inconnue. (codage/decodage)")
  except IOError:
    print("Fichiers source/code n'est pas dans le répertoire.")
  except TypeError:
    print("Seulement les fichiers .pgm sont acceptés.")
  except IndexError:
    print("Il manque au moins un argument.")
  except:
   print("Erreur inattendu.")


if __name__ == "__main__":
  main()
