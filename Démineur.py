################################################
#                                              #
#        Projet3  : Le Démineur                #
#        INFO-F-101 : Programmation            #
#        Matricule : 000396506                 #
#                                              #
################################################

__author__="Yasin Arslan (Matricule : 000396506)"
__date__="10 November 2014"
"""
   Petit jeu de démineur basé sur l'original de windows.
   Convention de sécurité : les coins ne cacheront jamais de bombe.
"""

from random import randint
#=========================
def print_grid(matrice):
#=========================
  """
  Fonction qui affiche la matrice ainsi que les coordonées choisi.
  """
  print(5*" ",end="")
  for countL in range(1,SIZE+1):
    print(countL, end=3*" ")
  print()
  for i in range(len(matrice)):
    print(3*" "+"-------------------------------------\n",chr(ord("A")+i),"|",end=" ")
    for j in range(len(matrice[0])):
      print(matrice[i][j],end=" | ")
    print()
  print(3*" "+"------------------------------------- ")

#==========================
def plant_bomb():
#==========================
  """
  Mise de bombe dans un dico. Le nombre de bombe est calculé par rapport à la difficulté voulu.
  Facile (5 bombes),Difficile(15 bombes) ou encore celle de l'énoncé (10 bombes)
  """
  grid = {}
  #Differente valeur possible pour la difficulté.
  easy_game = "0"
  hard_game = "1"
  standart = "2"
  print("Choose your difficulty.\nFor easy press",easy_game,", hard press",hard_game,", grid of projet3 press",standart,end=" : ")
  difficulty_choice = input()
  #####
  while not difficulty_choice.isdigit() or difficulty_choice not in (easy_game,hard_game,standart):
    print(" For easy press",easy_game,", hard press",hard_game,", grid of projet3 press",standart,end=" : ")
    difficulty_choice = input()
  #####
  #Grille par défaut, donné dans l'énoncé.
  if difficulty_choice == standart:
    grid[(0 ,7)] = BOMB
    grid[(1 ,5)] = BOMB
    grid[(1 ,6)] = BOMB
    grid[(1 ,8)] = BOMB
    grid[(2 ,4)] = BOMB
    grid[(3 ,4)] = BOMB
    grid[(5 ,5)] = BOMB
    grid[(5 ,7)] = BOMB
    grid[(7 ,0)] = BOMB
    grid[(7 ,5)] = BOMB
    bomb_count = 10          # 10 bombs.
    print("We planted ",bomb_count,"bombs. Good luck ! ")
  
  #Mode Facile.
  elif difficulty_choice == easy_game:
    bomb_count = 5           # 5 bombs.
    print("We planted ",bomb_count,"bombs. Good luck ! ")
  #Mode Difficile.
  else:
    bomb_count = 15          # 15 bombs.
    print("We planted ",bomb_count,"bombs. Good luck ! ")
  
  #Si Facile/Difficile, on aura besoin de spécifier les places des bombes\
  #via randint.
  if difficulty_choice in (easy_game,hard_game):    
    for i in range(bomb_count):
      bomb_position = ( randint(0,SIZE-1),randint(0,SIZE-1) )
      #On ne place pas deux bombes dans une même case, et on ne place \
      #pas de bombe dans les coins de notre tableau.
      #####
      while bomb_position in grid or bomb_position in {(0,0),(0,SIZE-1),(SIZE-1,0),(SIZE-1,SIZE-1)}:
        bomb_position = ( randint(0,SIZE-1),randint(0,SIZE-1) )
      #####
      grid[bomb_position] = BOMB  
  
  return grid

#======================================
def verify_bombs(grid,position):
#======================================
  """
  Fonction qui vérifie les cases adjacentes à la case selectionné.
  Si une bombe se trouve autour, un compteur sera mis à jour.
  Ce compteur affichera le nombre de bombe adjacent à la case.
  """
  count = 0
  #On va chercher autour de la case les eventuelles bombes.
  for i in range(-1,2):
    line_border = position[0]+i
    for j in range(-1,2):
      column_border = position[1]+j
      if (line_border,column_border) in grid:
        count+=1
  return count
#=========================================
def verify_around_bombs(matrice,grid,position):
#=========================================
  """
  Fonction qui verifie les case adjacentes aux cases adjacentes à la case de départ \
  si celle-ci n'avait aucune bombe autour d'elle
  """
  for i in range(-1,2):
    new_line = position[0] + i
    if 0<=new_line<SIZE:
      for j in range(-1,2):
        new_column = position[1] + j
        if 0<=new_column<SIZE:
          new_position = (new_line,new_column)
          count_case = verify_bombs(grid,new_position)
          if count_case>0:
            matrice[new_position[0]][new_position[1]] = count_case
          else:
            matrice[new_position[0]][new_position[1]] = EMPTY
  return matrice    

#===================
def valid_case(grid,matrice):
#===================
  """
  Fonction supplémentaire permetant à l'utilisateur d'avoir un avancé \
  sur l'évolution de la partie.
  En lui affichant le nombre de cases à dévoiler sans bombe.
  """
  free_case = 0
  
  for i in range(len(matrice)):
    for j in range(len(matrice)):
      #On compte toutes les cases libres , pour donner l'info\
      #à l'utilisateur.
      if (i,j) not in grid and matrice[i][j] == FREE:
        free_case += 1
        
  return free_case
#==================
def inputs(matrice):
  """
  Demande à l'utilisateur la case qu'il aimerait dévoiler.
  Recommence la fonction si la case selectionné a déjà été selectionné.
  """
  print("Choose your line (A to",chr(ord("A")+SIZE-1),end=") : ")
  line_choice = input()
  ###
  while len(line_choice)>1 or not line_choice.isalpha() or ord(line_choice.upper())<ord("A") or ord(line_choice.upper())>(ord("A")+SIZE-1):
    print("One letter please (A to",chr(ord("A")+SIZE-1),end=") : ")
    line_choice = input()
  ###
  print("Choose your column (1 to",SIZE,end=") : ")
  column_choice = input()
  ###
  while not column_choice.isdigit() or int(column_choice)<1 or int(column_choice)>SIZE:
    print("Positive number please (1 to",SIZE,end=") : ")
    column_choice = input()
  ###

  line_choice = ord(line_choice.upper())-ord("A")
  column_choice = int(column_choice)-1
  
  #Si la case choisi à déjà été ouverte, on recommence.
  if matrice[line_choice][column_choice] != FREE:
    print("You can only choose free cases (",FREE,") !")
    line_choice,column_choice = inputs(matrice)

  return (line_choice,column_choice)

#===============================
def next_turn(grid,matrice):
#===============================
  """
  Suite du jeu, jusqu'à la victoire ( toutes les cases sans bombes ) \
  ou défaite ( selectionner un case avec bombe )
  """
  flag = True
  ROUND = 1
  free_case = valid_case(grid,matrice)
  #La condition ici ne sera plus respecté uniquement en cas win/lose.
  while flag:
    #Pour un affichage plus correcte, on affiche le tour correspondant.
    #Le nombre de case à dévoiler également.
    print("### Round",ROUND)
    print("-->",free_case,"cases to find.")

    chosen_position = inputs(matrice)

    #Bombe -> Défaite.
    if chosen_position in grid:
      matrice[chosen_position[0]][chosen_position[1]] = BOMB
      flag = False
    #Libre -> Victoire ou tour suivant.
    else:
      count = verify_bombs(grid,chosen_position)
      if count==0:
        matrice[chosen_position[0]][chosen_position[1]] = EMPTY
        matrice = verify_around_bombs(matrice,grid,chosen_position)
      else:
        matrice[chosen_position[0]][chosen_position[1]] = count

    #On affiche le tableau après la modification de ce tour.
    print_grid(matrice)    
    free_case = valid_case(grid,matrice)
    #Defaite.
    if not flag:
      print("###\nBOUM, You lost !\n###")
    #Victoire.
    elif free_case == 0:
      print("###\nCONGRATULATIONS, You won !\n###")
      flag=False
    #Suite du jeu.
    else:
      ROUND += 1      
#============
def main():
#============
  matrice = [[FREE for i in range(SIZE)] for j in range(SIZE)]
  
  print("This is the standart free grid.")
  print_grid(matrice)
  grid = plant_bomb()
  next_turn(grid,matrice)
  
#====Global====#
BOMB = "B"
EMPTY = " "
FREE = "#"
SIZE = 9

if __name__ == "__main__" :
  print("###\nWelcome in the minesweeper game.\nTry to find all cases without bombs.\
        \nGood luck !\n###")
  main()
