# Utiliser MongoDB avec Python

MongoDB est une base de données NoSQL populaire largement utilisée pour stocker et gérer des données non structurées. Avec Python, vous pouvez facilement interagir avec MongoDB grâce à PyMongo, le driver officiel pour MongoDB. Cet article fournit un aperçu complet de l'utilisation de MongoDB avec Python, en abordant les concepts clés et en fournissant des exemples de code pratiques.

## Introduction à MongoDB

MongoDB est une base de données orientée documents qui stocke les données dans des collections flexibles similaires à des objets JSON. Cette approche non relationnelle offre une plus grande flexibilité et une meilleure évolutivité pour les applications modernes qui manipulent des données non structurées ou semi-structurées. MongoDB est particulièrement populaire dans le développement Web, les applications mobiles, les systèmes de gestion de contenu et les applications de données Internet.

## Installation de PyMongo

Avant de commencer à travailler avec MongoDB dans Python, vous devez installer PyMongo, le driver officiel recommandé pour interagir avec MongoDB à partir de Python. Vous pouvez l'installer facilement à l'aide de pip, le gestionnaire de paquets Python :

```
pip install pymongo
```

## Connexion à MongoDB

La première étape consiste à établir une connexion avec MongoDB. Voici un exemple de code pour vous connecter à une instance MongoDB locale :

```python
from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Accès à une base de données
db = client.nom_de_la_base
```

Dans cet exemple, nous créons d'abord une instance de `MongoClient` en fournissant l'URL de connexion à MongoDB. Ensuite, nous accédons à une base de données spécifique en utilisant l'attribut `db`. Si la base de données n'existe pas, MongoDB la créera automatiquement lors de la première insertion de données.

## Opérations CRUD

PyMongo vous permet d'effectuer facilement des opérations CRUD (Create, Read, Update, Delete) sur vos données MongoDB. Voici quelques exemples détaillés :

### Créer (Insérer) un document

```python
# Définir un nouveau document
nouveau_document = {"nom": "John Doe", "age": 30, "adresse": {"ville": "New York", "pays": "États-Unis"}}

# Insérer le document dans la collection "utilisateurs"
resultat = db.utilisateurs.insert_one(nouveau_document)
print(f"Document inséré avec l'ID : {resultat.inserted_id}")
```

Dans cet exemple, nous créons un nouveau document avec des champs tels que `nom`, `age` et `adresse` (qui est un sous-document). Ensuite, nous insérons ce document dans la collection `utilisateurs` à l'aide de la méthode `insert_one`. La méthode renvoie un objet `InsertOneResult` contenant l'ID du document nouvellement inséré.

### Lire des documents

```python
# Récupérer tous les documents de la collection "utilisateurs"
utilisateurs = db.utilisateurs.find()

# Itérer sur les résultats
for utilisateur in utilisateurs:
    print(utilisateur)
```

La méthode `find` sans arguments récupère tous les documents de la collection `utilisateurs`. Vous pouvez également utiliser des filtres pour récupérer des documents spécifiques. Par exemple, `db.utilisateurs.find({"age": {"$gt": 30}})` récupérera les documents où le champ `age` est supérieur à 30.

### Mettre à jour un document

```python
# Mise à jour du champ "age" pour un utilisateur spécifique
resultat = db.utilisateurs.update_one(
    {"nom": "John Doe"},
    {"$set": {"age": 31}}
)
print(f"{resultat.modified_count} document(s) mis à jour.")
```

Dans cet exemple, nous mettons à jour le champ `age` pour le document où le champ `nom` est égal à "John Doe". La méthode `update_one` prend deux arguments : le filtre de sélection et les modifications à apporter. Ici, nous utilisons l'opérateur `$set` pour définir le nouveau champ `age`.

### Supprimer un document

```python
# Supprimer un document spécifique
resultat = db.utilisateurs.delete_one({"nom": "John Doe"})
print(f"{resultat.deleted_count} document(s) supprimé(s).")
```

La méthode `delete_one` supprime le premier document correspondant au filtre spécifié. Dans cet exemple, nous supprimons le document où le champ `nom` est égal à "John Doe".

## Intégration avec des frameworks Web Python

De nombreux frameworks Web Python populaires, comme Django, Flask et Pyramid, offrent une intégration avec MongoDB via des Object Document Mappers (ODM) tels que MongoEngine et PyMongo-Motor. Ces ODM fournissent une couche d'abstraction, permettant aux développeurs d'interagir avec MongoDB en utilisant des objets Python au lieu d'écrire des requêtes brutes.

Voici un exemple d'utilisation de MongoEngine avec Django :

```python
from mongoengine import Document, StringField, IntField

class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True)
    age = IntField()

# Créer un nouvel utilisateur
user = User(username='johndoe', email='johndoe@example.com', age=30)
user.save()

# Récupérer un utilisateur
user = User.objects(username='johndoe').first()
print(user.email)  # johndoe@example.com
```

Dans cet exemple, nous définissons un modèle `User` en utilisant MongoEngine. Nous pouvons ensuite créer un nouvel utilisateur, l'enregistrer dans la base de données, et récupérer des utilisateurs existants en utilisant des requêtes similaires à celles utilisées avec les modèles Django.

Pour en apprendre davantage sur le développement d'applications Web complètes, vous pouvez consulter notre article [**CSS, la relève de Bootstrap ?**](https://tim-tek.com/2020/10/20/css-la-releve-de-bootstrap/), qui explore les dernières évolutions de CSS et son potentiel pour remplacer des frameworks CSS comme Bootstrap.

## Multiprocessing avec PyMongo

Lorsque vous utilisez le multiprocessing avec PyMongo, il est important de créer une nouvelle instance de `MongoClient` pour chaque processus. `MongoClient` gère le pooling de connexions en interne et n'est pas "fork-safe", ce qui signifie qu'il ne peut pas être partagé entre les processus.

```python
from pymongo import MongoClient
from multiprocessing import Pool

def create_connection():
    return MongoClient('mongodb://localhost:27017/')

def consumer(index_line):
    client = create_connection()
    users = client.database.users
    user = get_user(index_line["_id"])
    if user:
        users.insert_one(user)

def main():
    client = create_connection()
    index = client.database.index
    pool = Pool(10)  # Créer un pool de 10 processus de travail
    cursor = index.find({})
    pool.map(consumer, cursor)

if __name__ == "__main__":
    main()
```

Dans cet exemple, nous définissons une fonction `create_connection` pour créer une nouvelle instance de `MongoClient`. Dans la fonction `consumer`, nous appelons cette fonction pour obtenir une connexion client dédiée pour chaque processus. Ensuite, nous effectuons des opérations sur la base de données MongoDB en utilisant cette connexion.

Dans la fonction `main`, nous créons un pool de 10 processus de travail à l'aide de `multiprocessing.Pool`. Nous récupérons ensuite tous les documents de la collection `index` et utilisons la méthode `map` pour appliquer la fonction `consumer` à chaque document en parallèle.

## Requêtes avec expressions régulières

PyMongo vous permet d'utiliser des expressions régulières dans vos requêtes en important le module `re` et en compilant le motif d'expression régulière.

```python
import re
regex = re.compile("^foo", re.IGNORECASE)
db.users.find_one({"username": regex})
```

Dans cet exemple, nous compilons une expression régulière pour correspondre aux chaînes de caractères commençant par "foo" (sans tenir compte de la casse). Nous utilisons ensuite cette expression régulière dans le filtre de la méthode `find_one` pour récupérer le premier document où le champ `username` correspond à l'expression régulière.

## Combiner des opérateurs de requête

PyMongo prend en charge la combinaison de différents opérateurs de requête, comme `$in` et `$regex`, pour créer des requêtes plus complexes.

```python
import re
db.col.find({'music_description': {'$in': [re.compile('.*heavy.*'), re.compile('.*metal.*')]}})
```

Cette requête trouve les documents dans la collection `col` où le champ `music_description` correspond aux expressions régulières pour "heavy" ou "metal". Nous utilisons l'opérateur `$in` pour vérifier si le champ `music_description` correspond à l'une des expressions régulières fournies dans la liste.

## Bonnes pratiques et optimisations

Lors de l'utilisation de MongoDB avec Python, il est important de suivre les bonnes pratiques pour garantir des performances optimales et une utilisation efficace des ressources. Voici quelques conseils :

- **Indexation** : Créez des index sur les champs fréquemment utilisés dans les requêtes pour améliorer les performances de recherche.
- **Requêtes efficaces** : Évitez les requêtes trop larges ou complexes qui peuvent ralentir les performances. Filtrez les résultats autant que possible.
- **Gestion des connexions** : Réutilisez les connexions MongoDB autant que possible au lieu de créer une nouvelle connexion pour chaque opération.
- **Sécurité** : Implémentez des mécanismes de sécurité appropriés, tels que l'authentification, le contrôle d'accès et le chiffrement des données sensibles.
- **Validation des données** : Validez les données avant de les insérer dans MongoDB pour garantir l'intégrité et la cohérence des données.
- **Surveillance des performances** : Surveillez les performances de votre application MongoDB et ajustez les paramètres de configuration si nécessaire.

Avant de déployer une solution MongoDB en production, il peut être judicieux de réaliser une Preuve de Concept (POC) pour valider l'adéquation de la technologie à vos besoins spécifiques. Pour en savoir plus sur les POC, consultez notre article [**C'est quoi un POC ?**](https://tim-tek.com/2020/11/29/cest-quoi-un-poc/).

## Lecture complémentaire

Pour approfondir vos connaissances sur l'utilisation de MongoDB avec Python, voici quelques ressources fiables :

- [PyMongo Documentation](https://pymongo.readthedocs.io/en/stable/)
- [MongoDB Python Drivers](https://www.mongodb.com/docs/drivers/python-drivers/)
- [MongoDB PyMongo Tutorial](https://www.mongodb.com/resources/languages/pymongo-tutorial)

Ces ressources officielles de MongoDB vous aideront à maîtriser l'utilisation de PyMongo et à intégrer efficacement MongoDB dans vos applications Python.