#http://pascal.ortiz.free.fr/contents/tkinter/tkinter/le_canevas
import tkinter as tk
import tkinter.simpledialog as sd
import tkinter.messagebox as messagebox

class Damier:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.joueur_actuel = "B"
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.clic)
        self.draw_damier()
        self.pion_selectionne = None
        self.le_pion=None
        self.pt_joueur1=20
        self.pt_joueur2=20
        self.prise = []
        
        # Ajout du bouton "Quitter"
        self.btn_quitter = tk.Button(root, text="Quitter", command=root.quit)
        self.btn_quitter.pack(side="left")
        
        # Ajout du bouton "Nouvelle partie"
        self.btn_nouvelle_partie = tk.Button(root, text="Nouvelle partie", command=self.nouvelle_partie)
        self.btn_nouvelle_partie.pack(side="right")
        
        
        
        
        
    def nouvelle_partie(self):
          # Supprimer les anciens labels
        if hasattr(self, "lbl_joueur"):
            self.lbl_joueur.pack_forget()
        if hasattr(self, "lbl_points_joueur1"):
            self.lbl_points_joueur1.pack_forget()
        if hasattr(self, "lbl_points_joueur2"):
            self.lbl_points_joueur2.pack_forget()
        # Demander les noms des deux joueurs
        self.joueur1 = sd.askstring("Nouvelle partie", "Entrez le nom du joueur 1:")
        self.joueur2 = sd.askstring("Nouvelle partie", "Entrez le nom du joueur 2:")
        if self.joueur1 and self.joueur2:
            # Réinitialiser le damier
            self.canvas.delete("all")
            self.draw_damier()
            self.init_jeu()
            # Ajout du label indiquant le joueur actuel
            self.lbl_joueur = tk.Label(root, text="Au tour de " + self.joueur1, font=("Arial", 14),fg="blue")
            self.lbl_joueur.pack(side="top", pady=10)
            # Ajout du compteur de points pour les deux joueurs
            self.lbl_points_joueur1 = tk.Label(root, text="Pions restants pour "+ self.joueur1 +" : " + str(self.pt_joueur1), font=("Arial", 12))
            self.lbl_points_joueur1.pack(side="top")
            
            self.lbl_points_joueur2 = tk.Label(root, text="Pions restants pour"+ self.joueur2 +" : " + str(self.pt_joueur2), font=("Arial", 12))
            self.lbl_points_joueur2.pack(side="top")
            # Réinitialiser le compteur de points
            self.pt_joueur1 = 20
            self.pt_joueur2 = 20
            self.mettre_a_jour_points()
            
    def mettre_a_jour_points(self):
        self.lbl_points_joueur1.configure(text="Pions restants pour "+ self.joueur1 +" : " + str(self.pt_joueur1))
        self.lbl_points_joueur2.configure(text="Pions restants  pour "+ self.joueur2 +" : " + str(self.pt_joueur2))

   
    def draw_damier(self):
        taille_case = 50
        for i in range(10):
            for j in range(10):
                if (i+j) % 2 == 0:
                    color = "gray"
                else:
                    color = "white"
                self.canvas.create_rectangle(i*taille_case, j*taille_case, (i+1)*taille_case, (j+1)*taille_case, fill=color)

    def init_jeu(self):
        self.jeu = [[0 if (i+j) % 2 == 0 else 2 for j in range(10)] for i in range(10)]
        self.pion = [[0 for j in range(10)] for i in range(10)]
        for i in range(10):
            for j in range(10):
                if (i+j) % 2 == 0:
                    if i < 4:
                        self.pion[i][j] = "J"
                        self.draw_pion(i, j, "Orange")
                        self.jeu[i][j] = 1
                    elif i > 5:
                        self.pion[i][j] = "B"
                        self.draw_pion(i, j, "blue")
                        self.jeu[i][j] = 1

    def draw_pion(self, i, j, color):
        taille_case = 50
        
        self.canvas.create_oval(j*taille_case+5, i*taille_case+5, (j+1)*taille_case-5, (i+1)*taille_case-5, fill=color,width=2)
    
    def promouvoir_pion_en_dame(self, i, j):
        if self.pion[i][j] == "J" and i == 9:
            self.pion[i][j] = "J"
            self.canvas.delete(self.canvas.find_closest(j*50+25, i*50+25))
            self.draw_pion(i, j, "yellow")
            self.jeu[i][j] = 4
            
        elif self.pion[i][j] == "B" and i == 0:
            self.pion[i][j] = "B"
            self.canvas.delete(self.canvas.find_closest(j*50+25, i*50+25))
            self.draw_pion(i, j, "purple")
            self.jeu[i][j] = 4
      

    def supprimer_pion(self, i, j):
        self.canvas.delete(self.pion[i][j])
        self.jeu[i][j] = 0
        self.pion[i][j] = 0
        # Mettre à jour les points des joueurs
        if self.joueur_actuel == "J":
            self.pt_joueur2 -= 1
        else:
            self.pt_joueur1 -= 1

        self.mettre_a_jour_points()
        self.fin_jeu()
    
    def clic(self, event):
        i,j = event.y // 50, event.x // 50
        print("Case cliquée:",j,i)
        # Utilisation de la variable joueur_actuel pour autoriser uniquement les mouvements des pions appartenant au joueur en cours 
        if self.jeu[i][j] == 1  and self.pion[i][j] == self.joueur_actuel:
            self.le_pion=1
            if self.pion_selectionne:
                self.canvas.itemconfig(self.pion_selectionne[2], outline="black")
            # Sélectionner le nouveau pionsélectionné pour l'afficher en rouge     
            self.pion_selectionne = (i,j,self.canvas.find_closest(event.x,event.y)[0])
            self.canvas.itemconfig(self.pion_selectionne[2], outline='red')
        if self.jeu[i][j] == 4  and self.pion[i][j] == self.joueur_actuel:
                self.le_pion=4
                if self.pion_selectionne:
                    self.canvas.itemconfig(self.pion_selectionne[2], outline="black")
                # Sélectionner le nouveau pionsélectionné pour l'afficher en rouge     
                self.pion_selectionne = (i,j,self.canvas.find_closest(event.x,event.y)[0])
                self.canvas.itemconfig(self.pion_selectionne[2], outline='red')
        elif self.pion_selectionne and not (i,j) == (self.pion_selectionne[0],self.pion_selectionne[1]):
            if self.le_pion==1:
                deplacement_valide = self.deplacer_pion(self.pion_selectionne[0],self.pion_selectionne[1],i,j)
            elif self.le_pion==4:
                deplacement_valide = self.deplacer_dame(self.pion_selectionne[0],self.pion_selectionne[1],i,j)
            # Après chaque déplacement, passer au joueur suivant en changeant la valeur de joueur_actuel 
            if deplacement_valide:
                self.joueur_actuel = "B" if self.joueur_actuel == 'J' else 'J'
                # Mettre à jour le label indiquant le joueur actuel
                if self.joueur_actuel=="B":
                    self.lbl_joueur.configure(text="Au tour de " + self.joueur1+ " de jouer",fg="blue")
                else:
                    self.lbl_joueur.configure(text="Au tour de " + self.joueur2 + " de jouer",fg="Orange")
            # Supprimer le contour rouge après avoir terminé un déplacement
            self.canvas.itemconfig(self.pion_selectionne[2], outline="black")
            self.pion_selectionne=None
                 
    def deplacer_pion(self, i_dep, j_dep, i_arr, j_arr):
         if self.jeu[i_dep][j_dep] == 1 :
            if abs(i_arr - i_dep) == 1 and abs(j_arr - j_dep) == 1:
                direction = 1 if self.pion[i_dep][j_dep] == "J" else -1 # Déterminer la direction du mouvement
                if i_arr - i_dep == direction: # Vérifier que le déplacement est autorisé
                    if self.jeu[i_arr][j_arr] != 0:
                        return False # La case d'arrivée est déjà occupée par un pion
                    self.jeu[i_dep][j_dep] = 0
                    self.jeu[i_arr][j_arr] = 1
                    self.pion[i_arr][j_arr] = self.pion[i_dep][j_dep]
                    self.pion[i_dep][j_dep] = 0
                    self.canvas.move(self.canvas.find_closest(j_dep*50+25, i_dep*50+25), (j_arr-j_dep)*50, (i_arr-i_dep)*50)
                    self.promouvoir_pion_en_dame(i_arr,j_arr)
                    if abs(i_arr - i_dep) == 2: # Vérifier si le déplacement est un déplacement en arrière
                        i_pris = i_dep - direction
                        j_pris = (j_dep + j_arr) // 2
                        if self.pion[i_pris][j_pris] != 0 and self.pion[i_pris][j_pris] != self.pion[i_dep][j_dep]:
                            # Supprimer le pion pris en arrière
                            self.pion[i_pris][j_pris] = 0
                            self.canvas.delete(self.canvas.find_closest(j_pris*50+25, i_pris*50+25))
                            self.promouvoir_pion_en_dame(i_arr,j_arr)
                            # Mettre à jour les points des joueurs
                            if self.joueur_actuel == "J":
                                self.pt_joueur2 -= 1
                            else:
                                self.pt_joueur1 -= 1

                            self.mettre_a_jour_points()
                            self.fin_jeu()
                    return True
            else :
                while self.prise_possible_pion( i_dep, j_dep)== True and  abs(i_arr - i_dep) == 2 and abs(j_arr - j_dep) == 2:
                    self.manger(i_dep, j_dep, i_arr, j_arr)
                    self.promouvoir_pion_en_dame(i_arr,j_arr)
                    i_depart=i_arr
                    j_depart=j_arr
                    if self.prise_possible_pion( i_depart, j_depart)==True and  abs(i_arr - i_dep) == 2 and abs(j_arr - j_dep) == 2 :
                        self.manger(i_dep, j_dep, i_arr, j_arr)
                        self.promouvoir_pion_en_dame(i_arr,j_arr)
                    else:
                        return(True)
                               
            return(False)
     
    def manger(self, i_dep, j_dep, i_arr, j_arr):
        i_intermediaire = (i_dep + i_arr) // 2 # Calculer la position de la case intermédiaire
        j_intermediaire = (j_dep + j_arr) // 2
        if self.jeu[i_intermediaire][j_intermediaire] != 0 and self.pion[i_intermediaire][j_intermediaire] != self.pion[i_dep][j_dep]:
        # Si la case intermédiaire est occupée par un pion adverse, déplacer le pion et retirer le pion adverse
            self.jeu[i_dep][j_dep] = 0
            self.jeu[i_arr][j_arr] = 1
            self.jeu[i_intermediaire][j_intermediaire] = 0
            self.pion[i_arr][j_arr] = self.pion[i_dep][j_dep]
            self.pion[i_dep][j_dep] = 0
            self.canvas.move(self.canvas.find_closest(j_dep*50+25, i_dep*50+25), (j_arr-j_dep)*50, (i_arr-i_dep)*50)
            self.canvas.delete(self.canvas.find_closest(j_intermediaire*50+25, i_intermediaire*50+25))
            # Mettre à jour les points des joueurs
            if self.joueur_actuel == "J":
                self.pt_joueur2 -= 1
            else:
                self.pt_joueur1 -= 1

            self.mettre_a_jour_points()
            self.fin_jeu()
            
        
    def prise_possible_pion(self, i_dep, j_dep):
        if self.pion[i_dep][j_dep] == "J":
            direction = 1 # direction du mouvement pour les pions jaunes
        else:
            direction = -1 # direction du mouvement pour les pions bleus
        # Vérifier si la prise est possible en avant à gauche
        if i_dep+2*direction < 10 and j_dep-2 >= 0 and self.jeu[i_dep+2*direction][j_dep-2] == 0 and self.jeu[i_dep+direction][j_dep-1] != 0 and self.pion[i_dep+direction][j_dep-1] != self.pion[i_dep][j_dep]:
            return True
        # Vérifier si la prise est possible en avant à droite
        if i_dep+2*direction < 10 and j_dep+2 < 10 and self.jeu[i_dep+2*direction][j_dep+2] == 0 and self.jeu[i_dep+direction][j_dep+1] != 0 and self.pion[i_dep+direction][j_dep+1] != self.pion[i_dep][j_dep]:
            return True
        # Vérifier si la prise est possible en arrière à gauche
        if i_dep-2*direction >= 0 and j_dep-2 >= 0 and self.jeu[i_dep-2*direction][j_dep-2] == 0 and self.jeu[i_dep-direction][j_dep-1] != 0 and self.pion[i_dep-direction][j_dep-1] != self.pion[i_dep][j_dep]:
            return True
        # Vérifier si la prise est possible en arrière à droite
        if i_dep-2*direction >= 0 and j_dep+2 < 10 and self.jeu[i_dep-2*direction][j_dep+2] == 0 and self.jeu[i_dep-direction][j_dep+1] != 0 and self.pion[i_dep-direction][j_dep+1] != self.pion[i_dep][j_dep]:
            return True
        return False # Si aucune prise n'est possible, retourner False
    
    def deplacer_dame(self, i_dep, j_dep, i_arr, j_arr):
        pion_pris = []

        # Vérifier que la case d'arrivée est vide
        if self.jeu[i_arr][j_arr] != 0:
            return False

        # Vérifier que le déplacement est en diagonale
        if abs(i_arr - i_dep) != abs(j_arr - j_dep):
            return False

        # Vérifier que la dame ne saute pas d'autres pions
        i_direction = 1 if i_arr > i_dep else -1
        j_direction = 1 if j_arr > j_dep else -1
        i = i_dep + i_direction
        j = j_dep + j_direction

        # Prendre les pions sur le chemin
        while i != i_arr and j != j_arr:
            if self.pion[i][j] == self.joueur_actuel:
                return False
            if self.jeu[i][j] != 0:
                pion_pris.append((i, j))
            i += i_direction
            j += j_direction

        if len(pion_pris) > 1:
            return False

        if len(pion_pris) == 1:
            i_intermediaire, j_intermediaire = pion_pris[0]
            self.jeu[i_intermediaire][j_intermediaire] = 0
            self.pion[i_intermediaire][j_intermediaire] = 0
            self.canvas.delete(self.canvas.find_closest(j_intermediaire * 50 + 25, i_intermediaire * 50 + 25))
            # Mettre à jour les points des joueurs
            if self.joueur_actuel == "J":
                self.pt_joueur2 -= 1
            else:
                self.pt_joueur1 -= 1

            self.mettre_a_jour_points()
            self.fin_jeu()

        # Déplacer la dame
        self.jeu[i_dep][j_dep] = 0
        self.jeu[i_arr][j_arr] = 4
        self.pion[i_arr][j_arr] = self.pion[i_dep][j_dep]
        self.pion[i_dep][j_dep] = 0
        self.canvas.move(self.canvas.find_closest(j_dep * 50 + 25, i_dep * 50 + 25), (j_arr - j_dep) * 50,
                        (i_arr - i_dep) * 50)
        i_dep = i_arr
        j_dep = j_arr

        if self.prise_dame(i_dep, j_dep):
            pion_pris = []

            # Vérifier que la case d'arrivée est vide
            if self.jeu[i_arr][j_arr] != 0:
                return False

            # Vérifier que le déplacement est en diagonale
            if abs(i_arr - i_dep) != abs(j_arr - j_dep):
                return False

            # Vérifier que la dame ne saute pas d'autres pions
            i_direction = 1 if i_arr > i_dep else -1
            j_direction = 1 if j_arr > j_dep else -1
            i = i_dep + i_direction
            j = j_dep + j_direction

            # Prendre les pions sur le chemin
            while i != i_arr and j != j_arr:
                if self.jeu[i][j] != 0:
                    pion_pris.append((i, j))
                i += i_direction
                j += j_direction

            if len(pion_pris) > 1:
                return False

            if len(pion_pris) == 1:
                i_intermediaire, j_intermediaire = pion_pris[0]
                self.jeu[i_intermediaire][j_intermediaire] = 0
                self.pion[i_intermediaire][j_intermediaire] = 0
                self.canvas.delete(self.canvas.find_closest(j_intermediaire * 50 + 25, i_intermediaire * 50 + 25))
                # Mettre à jour les points des joueurs
                if self.joueur_actuel == "J":
                    self.pt_joueur2 -= 1
                else:
                    self.pt_joueur1 -= 1

            self.mettre_a_jour_points()
            self.fin_jeu()

            # Déplacer la dame
            self.jeu[i_dep][j_dep] = 0
            self.jeu[i_arr][j_arr] = 4
            self.pion[i_arr][j_arr] = self.pion[i_dep][j_dep]
            self.pion[i_dep][j_dep] = 0
            self.canvas.move(self.canvas.find_closest(j_dep * 50 + 25, i_dep * 50 + 25), (j_arr - j_dep) * 50,(i_arr - i_dep) * 50)
            # Mettre à jour les points des joueurs
            if self.joueur_actuel == "J":
                self.pt_joueur2 -= 1
            else:
                self.pt_joueur1 -= 1

        self.mettre_a_jour_points()
        self.fin_jeu() 
        return True
         
    def prise_dame(self, i_dep, j_dep):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] # directions possibles pour une dame
        for direction in directions:
            i_arr = i_dep + direction[0]
            j_arr = j_dep + direction[1]
            while self.est_valide(i_arr, j_arr):
                # Vérifier si la case d'arrivée contient un pion ou une dame de l'adversaire
                if self.jeu[i_arr][j_arr] != 0 and self.jeu[i_arr][j_arr] != self.jeu[i_dep][j_dep] :
                    i_pris = i_arr + direction[0]
                    j_pris = j_arr + direction[1]
                    # Vérifier si la case après le pion ou la dame de l'adversaire est vide
                    if self.est_valide(i_pris, j_pris) and self.jeu[i_pris][j_pris] == 0:
                        if self.pion[i_arr][j_arr] != self.joueur_actuel:
                            return True
                i_arr += direction[0]
                j_arr += direction[1]
        return False

    def est_valide(self, i, j):
        return 0 <= i < 10 and 0 <= j < 10
    
    def fin_jeu(self):
        if self.pt_joueur1 == 0:
            messagebox.showinfo("Fin de jeu", f"Le joueur {self.joueur2} a gagné !")
        elif self.pt_joueur2 == 0:
            messagebox.showinfo("Fin de jeu", f"Le joueur {self.joueur1} a gagné !")
            
    
    
    
root = tk.Tk()
root.title("Jeu de Dames")
damier = Damier(root)
root.mainloop()