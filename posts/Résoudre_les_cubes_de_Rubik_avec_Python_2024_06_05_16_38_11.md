# Résoudre les cubes de Rubik avec Python

Bienvenue à tous les passionnés de codage et de casse-tête ! Aujourd'hui, nous allons explorer comment résoudre le célèbre cube de Rubik en utilisant Python. Ce projet fascinant mêle vision par ordinateur, algorithmique et, bien sûr, un peu de magie.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les bibliothèques Python suivantes :

- **NumPy** : Pour la manipulation de tableaux numériques.
- **OpenCV** : Pour le traitement d'images et la vision par ordinateur.
- **rubikscubennnsolver** : Une bibliothèque contenant différents algorithmes de résolution de cubes.

Vous pouvez les installer avec `pip` :

```
pip install numpy opencv-python rubikscubennnsolver
```

## Introduction

Le cube de Rubik est un véritable défi pour les esprits les plus brillants. Avec ses 6 faces multicolores et ses mouvements complexes, il peut sembler insurmontable de le résoudre. Mais grâce à Python et à quelques bibliothèques puissantes, nous allons créer un programme capable de déchiffrer ce casse-tête emblématique.

## Détection des carrés colorés

La première étape consiste à détecter et identifier les carrés colorés sur chaque face du cube. Pour cela, nous utiliserons la bibliothèque OpenCV pour le traitement d'images. Voici les principales étapes :

1. **Conversion de l'image en espace de couleur HSV** : Cet espace de couleur sépare mieux les teintes (Hue), la saturation (Saturation) et la luminosité (Value), ce qui facilite la détection de couleurs spécifiques.
2. **Seuillage par couleur avec `cv2.inRange()`** : Nous définirons des plages de couleurs HSV pour détecter les carrés rouges, verts, bleus, etc.
3. **Opérations morphologiques** : Des techniques comme l'ouverture (érosion suivie d'une dilatation) et la fermeture (dilatation suivie d'une érosion) amélioreront la détection des contours en éliminant les petits trous ou défauts.
4. **Trouver les contours avec `cv2.findContours()`** : Nous obtiendrons ainsi les contours des carrés détectés.
5. **Calculer le facteur de "carritude"** : En comparant la hauteur et la largeur des contours, nous pourrons identifier les formes réellement carrées. Le facteur de carritude est calculé comme `min(largeur, hauteur) / max(largeur, hauteur)`. Une valeur proche de 1 indique un carré parfait.
6. **Trier les contours** : Nous organiserons les carrés détectés par position (haut, bas, gauche, droite) pour les mapper sur les faces du cube.

Voici un exemple de code pour détecter les carrés rouges :

```python
# Conversion en HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Seuillage pour le rouge
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])
mask_red = cv2.inRange(hsv, lower_red, upper_red)

# Opérations morphologiques
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)

# Trouver les contours
contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filtrer les contours carrés
squares = []
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    squareness = min(w, h) / max(w, h)
    if squareness > 0.9:  # Seuil de carritude à 0.9
        squares.append(cnt)
```

## Résolution du cube

Une fois que nous avons détecté et classé les carrés colorés, nous pouvons encoder l'état du cube sous forme de chaîne de caractères. Cette chaîne sera ensuite passée à une bibliothèque de résolution de cubes, comme Kociemba.

La bibliothèque Kociemba utilise un algorithme de recherche en profondeur d'abord pour trouver la séquence de mouvements la plus courte pour résoudre le cube. L'algorithme explore tous les mouvements possibles jusqu'à ce qu'une solution soit trouvée.

Voici un exemple de code pour résoudre le cube :

```python
from rubikscubennnsolver import utils

# Encodage de l'état du cube
encoding = "".join(utils.color_to_label[color] for color in sticker_colors)

# Résolution avec Kociemba
solution = utils.solve(encoding, "Kociemba")

# Affichage de la solution
print(f"Solution en {len(solution.split())} mouvements :")
print(solution)
```

Pour mieux visualiser le processus de résolution, vous pouvez implémenter une fonction permettant d'afficher l'état du cube à chaque étape, en appliquant les mouvements de la solution trouvée par Kociemba.

## Conclusion

Et voilà ! Nous avons maintenant un programme capable de résoudre n'importe quel cube de Rubik. N'est-ce pas fascinant de voir comment le codage et l'intelligence artificielle peuvent relever ce défi légendaire ? Bien que ce projet puisse sembler complexe au premier abord, en décomposant les étapes et en utilisant les bonnes bibliothèques, nous avons pu créer une solution élégante et efficace.

N'hésitez pas à explorer davantage ce sujet passionnant et à personnaliser le code pour répondre à vos besoins spécifiques. Vous pouvez par exemple ajouter une interface utilisateur graphique, intégrer des modèles d'apprentissage profond pour une détection de couleurs plus robuste, ou encore optimiser les algorithmes de résolution pour une performance accrue. Pour en savoir plus sur l'optimisation des performances et les techniques de programmation asynchrone en Python, consultez notre article [**Asynchronous Programming in Python**](https://tim-tek.com/async-python).

## Lecture complémentaire

Pour approfondir vos connaissances sur ce sujet passionnant, voici quelques ressources fiables :

- [Solving a Rubik's Cube with Python par Andrew Bauer](https://github.com/andrewbauer/rubiks-cube-solver)
- [How to Solve a Rubik's Cube with Python par PyImageSearch](https://pyimagesearch.com/2022/01/31/how-to-solve-a-rubiks-cube-with-python/) 
- [Rubik's Cube Solver with Python par Michael Muehlich](https://github.com/mdmuehli/rubiks-cube-solver)

Si vous êtes intéressé par les concepts de programmation asynchrone, qui peuvent être utiles pour optimiser les performances de votre programme, vous pouvez consulter notre article [**Comprehending Promises in JavaScript**](https://tim-tek.com/javascript-promises) pour en apprendre davantage.

N'hésitez pas à explorer ces ressources pour découvrir d'autres techniques et approches pour résoudre ce casse-tête fascinant avec Python. Amusez-vous bien et n'ayez pas peur de casser quelques cubes en chemin !