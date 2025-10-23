### Logiciel de traitement d'image ###
# Import de la bibliotheque Pillow et TKinter

from PIL import Image

### Fonctions ###

#niveau de gris
"""traitement classique de mise en niveau de gris d'une image
--->Cela signifie que les trois composantes ont la même valeur."""
def gris(image):
    for y in range(hauteur):
        for x in range(largeur):
            r, v, b = image.getpixel((x, y))
            image.putpixel((x, y) , (r, r, r))
    image.save("new_img.jpg")

def negatif(img): #transforme l'image en son négatif en inversant l'intensité de chaques couleurs de l'image.
    for y in range(hauteur): 
        for x in range(largeur): 
            r, v, b = img.getpixel((x, y)) 
            img.putpixel((x, y), (255 - v, 255 - b, 255 - r)) 
    img.save("new_img.jpg")

def filtre_rouge(img): # Fonction permettant d'appliquer un filtre rouge sur une image
    for y in range(hauteur): 
        for x in range(largeur): 
            r, v, b = img.getpixel((x, y)) 
            img.putpixel((x, y), (r, 0, 0))
    img.save("new-img.jpg")

#augmenter la luminosité
""" courbe tonale pour augmenter la luminosité
---> composantes les plus foncés =plus aucun point entre 0 et 96. 
---> composantes ayant une valeur supérieure à 160 = points blancs"""
def a_lum(img):
    lum = int(input("De combien voulez vous augmenter la luminosité ? "))
    for y in range(hauteur): 
        for x in range(largeur): 
            r, v, b = img.getpixel((x, y)) 
            img.putpixel((x, y), (r + lum, v + lum, b + lum)) 
    img.save("new_img.jpg")

def r_lum(img): #réduit la luminosité de l'image en soustraillant une valeur fixe à toute les composantes
    lum = int(input("De combien voulez vous diminuer la luminosité ? "))
    for y in range(hauteur): 
        for x in range(largeur): 
            r, v, b = img.getpixel((x, y)) 
            img.putpixel((x, y), (r - lum, v - lum, b - lum)) 
    img.save("new_img.jpg")

def contraste(img):
    """ permet de créer un contraste sur l'image """
    for y in range(hauteur):
        for x in range(largeur):
            r, v, b = img.getpixel((x, y))
            if r < 80:
                r = 0
            elif r > 140:
                r = 255
                    
            if v < 80:
                v = 0
            elif v > 140:
                v = 255
                    
            if b < 80:
                b = 0
            elif b > 140:
                b = 255
            img.putpixel((x, y), (r, v, b))
    img.save("new-img.jpg")
    
#seuillage
"""traitement plus complexe pour le seuillage d'une image
--->pixel à une valeur > au seuil alors = 255 (blanc)
--->pixel à une valeur < au seuil alors = 0 (noir). """
def seuillage(image):
    seuil_r= 123
    seuil_v= 123
    seuil_b= 123
    for y in range(hauteur):
        for x in range(largeur):
            r, v, b = image.getpixel((x, y))
            if r > seuil_r:
                r = 255
            else:
                r = 0
            if v > seuil_v:
                v = 255
            else:
                v = 0
            if b > seuil_b:
                b = 255
            else:
                b = 0
                image.putpixel((x, y) , (r, v, b)) 
    image.save("new_img.jpg")

def pixel(img): #change les nombre de pixels dont sera fait l'image en divisant sa résolution par 10 (regroupe 10 pixels en 1).
    pix = int(input("Quelle est la valeur de pixelisation ? "))
    for y in range(0, hauteur, pix): 
        for x in range(0, largeur, pix):
            new_r = 0
            new_v = 0
            new_b = 0
            for k in range(pix):
                for l in range(pix):
                    new_h = (y + k)
                    new_l = (x + l)
                    if new_h > hauteur:
                        new_h = hauteur - pix-1
                    if new_l > largeur:
                        new_l = largeur - pix-1
                    r, v, b = img.getpixel((new_l, new_h))
                    new_r += r
                    new_v += v
                    new_b += b
            for k in range(10):
                for l in range(10):
                    img.putpixel((x + k, y + l), (int(new_r//(pix*pix)), int(new_v//(pix*pix)), int(new_b//(pix*pix))))           
    img.save("new_img.jpg")

def sepia(img):
    """ permet la division de l'image """
    for y in range(hauteur):
        for x in range(largeur):
            r, v, b = img.getpixel((x, y))
            n_r = int(0.393 * r + 0.769 * v + 0.189 * b)
            n_v = int(0.349 * r + 0.686 * v + 0.168 * b)
            n_b = int(0.272 * r + 0.534 * v + 0.131 * b)
            img.putpixel((x, y), (n_r, n_v, n_b))
    img.save("new-img.jpg")

#lissage
"""traitement filtrage pour le lissage d'une image
--->Cela signifie rendre l'image plus fou = remplacerla valeur de chaque pixel par la moyenne
des 9 pixels formant un carré."""
def lissage(image):
    matrice = [[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]]
    for y in range(1, hauteur-1):
        for x in range(1, largeur-1):
            new_r = 0
            new_b = 0
            new_v = 0
            for k in range(len(matrice)):
                for l in range( len(matrice)):
                    r, v, b = image.getpixel((x+k -1, y+l-1))
                    new_r = new_r + int(r*matrice[k][l])
                    new_b = new_b + int(b*matrice[k][l])
                    new_v = new_v + int(v*matrice[k][l])
                      
                    image.putpixel((x, y) , (new_r, new_v, new_b))
    image.save("new_img.jpg")

def accentuation(img): #Rend l'image plus nette en remplacant la vleur de chaque pixel par la moyenne des 9 pixels formant un carré.
    matrice = [[0, -0.5, 0], [-0.5, 3, -0.5], [0, -0.5, 0]]
    for x in range(0, largeur - 2):
        for y in range(0, hauteur - 2):
            new_r = 0
            new_g = 0
            new_b = 0
            for i in range(len(matrice)):
                for j in range(len(matrice)):
                    r, g, b = img.getpixel((x - 1 + i, y - 1+ j))
                    new_r += int(r * matrice[i][j])
                    new_g += int(g * matrice[i][j])
                    new_b += int(b * matrice[i][j])
            img.putpixel((x, y), (new_r, new_g, new_b))
    img.save("new_img.jpg")

def gradiant(img):
    """ permet de réaliser le filtrage gradient grâce a une matrice """
    matrice = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    """permet de créer la matrice gradient"""   
    for y in range(0, hauteur-2):
        for x in range(0, largeur-2):
            n_r = 0
            n_v = 0
            n_b = 0
            for j in range (3):
                for i in range (3):
                    r, v, b = img.getpixel((x+i, y+j))
                    n_r = n_r + r*matrice[i][j]
                    n_v = n_v + v*matrice[i][j]
                    n_b = n_b + b*matrice[i][j]
                    img.putpixel((x, y), (n_r, n_v, n_b))
    
    img.save("new-img.jpg")

### Corps du programme ###

img = Image.open("img.jpg")
largeur, hauteur = img.size