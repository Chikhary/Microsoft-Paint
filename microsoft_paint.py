
# SPÉCIFICATION

# Un logiciel d'édition graphique "dessiner" s'apparentant à une version 
# simplifiée du logiciel Microsoft Paint qui permet à l'utilisateur de dessiner
# des rectangles de différentes tailles et différentes couleurs à l'aide de la 
# souris. Ce logiciel est developpé via la plateforme CodeBoot.

# CONCEPTION

# Le logiciel est composée de 6 sous-fonctions qui permet à l'utilisateur 
# éxecutant le code de dessiner des rectangles flottants de la couleur 
# souhaitée et de la taille souhaitée à l'aide d'appels de différentes 
# structures, qui sont données dans les fonctions "creerBoutons", 
# "trouverBoutons", de la procédure auxiliaire "creerImage", ainsi que d'autres
# structures dans des fonctions plus générales comme 
# "dessinerRectangleFlottant" et "ajouterRectangle". Ces fonctions permettent
# d'enregistrer les coordonnées des différentes coordonnées de l'éditeur placé
# en haut à droite et de commander au programme de suivre les différentes
# actions faites par la souris et de faire les changements souhaités dans
# l'éditeur.

# CODAGE

# Tableau contenant les couleurs affichées dans le menu.
couleurs = ["#fff", "#000", "#f00", "#ff0", "#0f0", "#00f", "#f0f"]
   

# *Remarque-CONCEPTION*
# La fonction principale dessiner() permet d'éxécuter le programme. Dès que
# l'utilisateur efface ses rectangles, dessiner() propose à celui-ci d'appeler
# la fonction.
def dessiner():
    # Apparition de l'éditeur, ainsi que la barre grise du menu.
    setScreenMode(180,120)
    fillRectangle(0, 0, 180, 120, "#fff")
    fillRectangle(0, 0, 180, 25, "#888")
   
    # Taille optimale des carrés de couleurs du menu,initialement noirs, mais
    # entièrement remplis de la couleur souhaitée ainsi que l'espace les 
    # séparant.
    taille = 12
    espace = taille // 2
    x = 6
    y = 6 
    x1 = x + 1
    y1 = y + 1
    for i in range(2*(len(couleurs))+1):
        if i % 2 == 0:
            fillRectangle(x, y, taille, taille, couleurs[1])
            x += taille + espace
        
    # Remplissage des carrés, initalement noirs, de leur couleur souhaitée.       
    for j in range(len(couleurs) + 1):
        if j >= 1:
            fillRectangle(x1, y1, taille - 2, taille - 2, couleurs[j-1])
            x1 += taille + espace
        else:
            fillRectangle(x1, y1, taille - 2, taille - 2, couleurs[j])
            x1 += taille + espace
        
    # Affichage des "points rouges" contenus dans le bouton servant à restaurer
    # le tableau blanc de l'éditeur.
    for i in range(2):
        xi = 6
        yi = 6
        for j in range(1, 11):
            if i == 0:
                setPixel(xi + j, yi + j, couleurs[2]) 
            else:
                setPixel(xi + taille -1- j, yi + j, couleurs[2])
    testDessiner()
    traiterProchainClic(creerBoutons(couleurs, taille, espace, couleurs[0]))
    imprimerFinProgramme = print("Rectangles effacés,\n \
                                 Pour recommencer : appel dessiner()")
    return imprimerFinProgramme
        
# *Remarque-CONCEPTION*
# La sous-fonction creerBoutons() permet d'implémenter les boutons dans le 
# menu du logiciel. Elle est donc composée de 4 paramètres, soit:
# 1- Un tableau d'enregistrement contenant les couleurs souhaitées dans le menu
# 2- La longueur/hauteur d'un bouton en forme de carré
# 3- L'espace entre les boutons du menu
# 4- La couleur pour le bouton effacé (le blanc est recommandé)
def creerBoutons(couleurs, taille, espace, couleurEffacer):
    if taille < 0 or espace < 0:
        return None
    # Variable boutonEffacer fourni dans l'énoncé
    boutonEffacer = struct(coin1 = struct(x = espace, y = espace), 
                           coin2 = struct(x = taille + espace, 
                                          y = taille + espace) ,
                           couleur = couleurEffacer, effacer = True)
    
    # Tableau contenant uniquement le boutonEffacer
    boutons = [boutonEffacer]
    
    # Implémentation de chaque bouton dans le tableau boutons. On utilise les 
    # paramètres "couleurs","taille" et "espace".
    for i in range(len(couleurs)):
        bond = (i + 1) * (espace + taille) 
        bouton = struct(coin1 = struct(x = boutonEffacer.coin1.x + bond,
                                       y = espace), 
                        coin2 = struct(x = boutonEffacer.coin2.x + bond, 
                                       y = boutonEffacer.coin1.y + taille) , 
                        couleur = couleurs[i], effacer = False)
        if bond > (180 - boutonEffacer.coin1.x):
            return None
        boutons.append(bouton)
    return boutons

    # *Remarque-CONCEPTION*
    # La sous-fonction trouverBouton() permet de retrouver les coordonnées des 
    # boutons dans le menu. Si la position entrée ne correspond pas aux 
    # coordoonées d'un bouton, elle renvoit None. Elle est composée de 2 
    # paramètres, soit:
    # 1- Un tableau d'enregistrement contenant tous les boutons du menu
    # 2- Une position/coordonnée (x,y) 
def trouverBouton(boutons, position):
    # Variable coordonnee qui prend le rôle de "position" dans l'énoncé. On
    # utilise le paramètre "position".
    
    coordonnee = struct(x = position[0], y = position[1])
    
    # Implémentation des coordonnées dans chaque bouton du menu. On utilise 
    # le paramètre "boutons".
    for i in range(len(boutons)):
        if coordonnee.x >= boutons[i].coin1.x \
        and coordonnee.x <= boutons[i].coin2.x:
            if coordonnee.y >= boutons[i].coin1.y \
            and coordonnee.y <= boutons[i].coin2.y:
                return boutons[i]
    else:
         return None

# Cette fonction est une procédure auxiliaire permettant de définir 
# "imageOriginale0, qui est la matrice dont les coordonnées, données dans une
# matrice 180x120, contient initialement la couleur blanche dans toutes ses
# coordonnées, mais est mise à jour dans "Image" et contient les
# coordonnées des rectangles dessinés par la personne qui lance le code.
# Cette fonction est fortement reprise de la fonction creerMatrices, créée par
# Marc Feeley et partagée dans la diapo 8 du cours.
def imageCreee(nbRangees, nbColonnes):
    resultat = [None] * nbRangees
    for i in range(nbRangees):
        resultat[i] = ["#fff"] * nbColonnes
    return resultat

imageOriginale0 = imageCreee(180,120)


# Cette fonction est au coeur du programme. Cette fonction reprend les
# coordonnées de la souris sur l'éditeur, à l'aide de la fonction getMouse,
# et attent que le spectateur appuie sur la le bouton gauche de la souris pour 
# qu'il se mette a dessiner les rectangles dirigés par la souris. La première
# partie du code n'appelle que la fonction fillRectangle, mais la deuxième
# appelle les fonctions restaurerImage et ajouterRectangle, pour permettre au
# spectateur d'effacer les rectangles en surplus lorsqu'il diminue la taille
# de son rectangle et affiche de nouveau les rectangles qui étaient cachés par 
# ce rectangle en conception.
def dessinerRectangleFlottant(imageOriginale, debut, couleur):
    while True:
        if getMouse().button == 1:
            # Premières coordonnées de la souris lorsque le bouton gauche est
            # appuyé.
            debut = struct(x = getMouse().x, y = getMouse().y)
            while getMouse().button == 1 and getMouse().y > 25:
                # Coordonnées de la souris lorsque la souris est en train
                # d'avancer et lorsqu'elle est au dessus du menu
                x=getMouse().x
                y=getMouse().y
                # Couples permettant de déduire si la souris si la souris se
                # dirige vers la souris va vers les x négatifs ou les x 
                # positifs et est réutilisée dans les variables de distance en 
                # x et en y pour ne pas qu'il y ait de distance négative.
                coupleDebutX = min(debut.x, x)
                coupleDebutY = min(debut.y, y)
                coupleFinX = max(debut.x, x)
                coupleFinY = max(debut.y, y)
                # Variables calculant la distance parcourue en x et en y,peu
                # importe la direction choisie selon la souris pour le
                # spectateur
                distanceX = coupleFinX - coupleDebutX
                distanceY = coupleFinY - coupleDebutY
                # Affichage du rectangle dans l'éditeur
                fillRectangle(coupleDebutX, coupleDebutY, distanceX, distanceY,
                              couleur)
                sleep(0.01)
                # Actions à accomplir si le spectateur veut revenir sur ses pas
                # Le if vérifie si la distance concernant la position iniiale
                # du rectangle en x et en y est plus petite que la distance
                # en x et en y à l'instant précédent et appelle la fonction
                # "restaurerImage" pour restaurer les rectangles en surplus
                if abs(debut.x - getMouse().x) < distanceX or \
                abs(debut.y - getMouse().y) < distanceY and getMouse().y > 25:
                    # rectangle défini par les structures coin1 et coin2, qui
                    # sont elles-mêmes des structures contenant une valeur x et
                    # y.Le premier rectangle défini est le rectangle en surplus
                    # où la distance en y ne change pas, mais la distance en x
                    # change. L'appel à la fonction restaurerImage reprend donc
                    # ce rectangle et restaure ses couleurs avant que le 
                    # nouveau rectangle se crée.
                    rectangle = struct(coin1 = struct(x = min(x,getMouse().x),
                                                      y = min(debut.y, y)),
                                       coin2 = struct(x = max(x, getMouse().x),
                                                      y = max(debut.y, y)))
                    restaurerImage(imageOriginale, rectangle)
                    # Ce second rectangle représente le rectangle en surplus
                    # lorsque la distance en y change,mais la distance en x ne
                    # change pas.L'appel à la fonction restaurerImage reprend 
                    # donc ce rectangle et restaure ses couleurs avant que le 
                    # nouveau rectangle se crée.Ce rectangle est un complément
                    # du rectangle recréé juste avant.
                    rectangle = struct(coin1 = struct(x = min(x, debut.x),
                                                      y = min(getMouse().y, y))
                                       ,coin2 = struct(x = max(x, debut.x),
                                                       y = max(getMouse().y, 
                                                               y)))
                    restaurerImage(imageOriginale0, rectangle)
                if not getMouse().button == 1:
                    # Actions à accomplir pour que la couleur du rectangle créé 
                    # soit enregistré dans la matrice "imageOriginale" dans
                    # les coordonnées correspondant aux pixels du rectangle
                    # créé.
                    rectangle = struct(coin1 = struct(x = min(debut.x,
                                                              getMouse().x), 
                                                      y = min(getMouse().y, 
                                                              debut.y)), 
                                       coin2 = struct(x = max(debut.x, 
                                                              getMouse().x), 
                                                      y = max(getMouse().y, 
                                                              debut.y)))
                    
                    ajouterRectangle(imageOriginale0, rectangle, couleur)
                    break
        break
            
# Cette fonction change la couleur des pixels des positions i et j
# pour remettre la couleur initiale enregistrée dans la matrice
# imageOriginale dans les coordonnées conformes aux distances définies
# par le rectangle.Elle remet la couleur avant le passage du nouveau rectangle
# dans l'intervalle tracée par le rectangle.Cette fonction est réutilisée dans
# la fonction "dessinerRectangleFlottant".
def restaurerImage(imageOriginale, rectangle):
    for i in range(rectangle.coin1.x, rectangle.coin2.x + 1):
        for j in range(rectangle.coin1.y, rectangle.coin2.y + 1):
            setPixel(i, j, imageOriginale0[i][j])
                   
# Cette fonction met à jour la matrice "ImageOriginale0" pour indiquer aux
# coordonnées ayant leur couleur modifiée la nouvelle couleur en ces points.
def ajouterRectangle(image, rectangle, couleur):
    for i in range(rectangle.coin1.x, rectangle.coin2.x + 1):
        for j in range(rectangle.coin1.y, rectangle.coin2.y + 1):
            imageOriginale0[i][j] = couleur

# *Remarque-CONCEPTION*
# L'abstraction procedurale traiterProchainClic permet de recueillir 
# l'information sur le clic de l'utilisateur. 
def traiterProchainClic(boutons):
    couleur = couleurs[0]
    while getMouse():
        sleep(0.01)
        if getMouse().button == 1 and  getMouse().y <= 24:
            bouton = trouverBouton(boutons, (getMouse().x,getMouse().y))
            if bouton == None:
                continue
            if bouton.effacer == True:
                fillRectangle(0, 25, 180, 95, "#fff")
                break
            else:
                couleur = bouton.couleur
        else:
            dessinerRectangleFlottant(imageOriginale0, 0, couleur)
            
# Tests

def testDessiner():
    # Tests unitaires pour la sous-fonction creerBoutons()
    assert creerBoutons([], 0, 0, "#fff") == [struct(coin1 = struct(x = 0, 
                                                                    y = 0), 
                                                     coin2 = struct(x = 0, 
                                                                    y = 0) , 
                                                     couleur = "#fff", 
                                                     effacer = True)]
    assert creerBoutons(["#fff"], 2, 0, "#fff") == [struct(
        coin1 = struct(x = 0, y = 0), coin2 = struct(x = 2, y = 2) ,
        couleur = "#fff", effacer = True), struct(
        coin1 = struct(x = 2, y = 0), coin2 = struct(x = 4, y = 2) , 
        couleur = "#fff", effacer = False)]
    assert creerBoutons(["#000"], 5, 10, "#ff0") == [struct(
        coin1 = struct(x = 10, y = 10), coin2 = struct(x = 15, y = 15) ,
        couleur = "#ff0", effacer = True), struct(
        coin1 = struct(x = 25, y = 10), coin2 = struct(x = 30, y = 15) ,
        couleur = "#000", effacer = False)]
    assert creerBoutons(["#f0f", "#0f0"], 20, 20, "#fff") == [struct(
        coin1 = struct(x = 20, y = 20), coin2 = struct(x = 40, y = 40) , 
        couleur = "#fff", effacer = True), struct(
        coin1 = struct(x = 60, y = 20), coin2 = struct(x = 80, y = 40) , 
        couleur = "#f0f", effacer = False), struct(
        coin1 = struct(x = 100, y = 20), coin2 = struct(x = 120, y = 40) ,
        couleur = "#0f0", effacer = False)]
    assert creerBoutons(["#00f"], 50, 100, "#fff") == None # Out of range

    # Tests unitaires pour la sous-fonction trouverBouton()
    assert trouverBouton([], (0,0)) == None # Impossible car 
                                            # pas de boutonEffacer
        
    assert trouverBouton(creerBoutons([], 10, 5, "#fff"), (7, 5)) == struct(
        coin1 = struct(x = 5, y = 5), coin2 = struct(x = 15, y = 15), 
        couleur = "#fff", effacer = True)
    assert trouverBouton(creerBoutons(["#000"], 5, 20, "#fff"), (50, 25)) == \
    struct(coin1 = struct(x = 45, y = 20), coin2 = struct(x = 50, y = 25), 
           couleur = "#000", effacer = False)
    assert trouverBouton(creerBoutons(["#0f0", "#f0f" ], 10, 3, "#fff"), 
                         (0, 10)) == None
    assert trouverBouton(creerBoutons(["#f00", "#ff0", "#0f0"], 12, 6, "#fff"),
                         (125, 50)) == None 
    
    # Tests unitaires pour la procédure restaurerImage()
    
    
    # Tests unitaires pour la procédure ajouterRectangle()
    assert ajouterRectangle(imageCreee(180,120), struct(
        coin1  = struct(x = 0, y = 30), coin2 = struct(x = 2, y = 40)),
                            "#000") == None
    assert ajouterRectangle(imageCreee(180,120), struct(
        coin1  = struct(x = 5, y = 30), coin2 = struct(x = 10, y = 50)), 
                            "#000") == None
    assert ajouterRectangle(imageCreee(180,120), struct(
        coin1  = struct(x = 0, y = 30), coin2 = struct(x = 15, y = 40)), 
                            "#f00") == None
    assert ajouterRectangle(imageCreee(180,120), struct(
        coin1  = struct(x = 10, y = 30), coin2 = struct(x = 5, y = 35)),
                            "#ff0") == None
    assert ajouterRectangle(imageCreee(180,120), struct(
        coin1  = struct(x = 0, y =45), coin2 = struct(x = 2, y = 40)), 
                            "#0f0") == None
    assert ajouterRectangle(imageCreee(180,120), struct(
        coin1  = struct(x = 15, y = 60), coin2 = struct(x = 10, y = 70)), 
                            "#00f") == None
    assert ajouterRectangle(imageCreee(180,120), struct(
        coin1  = struct(x = 20, y = 70), coin2 = struct(x = 30, y = 85)), 
                            "#000") == None
    
                         
dessiner()