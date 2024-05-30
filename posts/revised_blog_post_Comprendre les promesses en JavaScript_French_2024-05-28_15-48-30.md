# Comprendre les promesses en JavaScript

Les promesses (promises en anglais) sont un concept clé en JavaScript qui permet de gérer efficacement le code asynchrone. Dans cet article, nous allons explorer en détail ce que sont les promesses, leur fonctionnement et leur utilisation. Alors, prêts à découvrir ce puissant outil ?

## Qu'est-ce qu'une promesse ?

Une promesse est un objet JavaScript qui représente le résultat potentiel d'une opération asynchrone. En d'autres termes, c'est une façon de gérer le code qui s'exécute de manière non bloquante, comme les requêtes AJAX, les opérations de lecture/écriture de fichiers, etc.

Traditionnellement, le code asynchrone était géré à l'aide de callbacks, mais cette approche pouvait rapidement devenir complexe et difficile à maintenir, surtout avec des callbacks imbriqués (aussi connus sous le nom de "callback hell"). Les promesses offrent une solution plus élégante et lisible pour gérer ces opérations asynchrones.

## États d'une promesse

Une promesse peut se trouver dans l'un des trois états suivants :

1. **Pending** (en attente) : C'est l'état initial d'une promesse lorsqu'elle est créée et que l'opération asynchrone est en cours d'exécution.
2. **Fulfilled** (résolue) : La promesse est résolue lorsque l'opération asynchrone s'est terminée avec succès.
3. **Rejected** (rejetée) : La promesse est rejetée lorsque l'opération asynchrone a rencontré une erreur.

Une promesse ne peut être que dans un seul état à la fois, et son état final ne peut pas être modifié ultérieurement.

## Créer une promesse

Pour créer une promesse, vous devez utiliser le constructeur `Promise`. Il prend une fonction exécutrice (executor) comme argument, qui elle-même prend deux paramètres : `resolve` et `reject`. Cette fonction exécutrice contient le code asynchrone que vous souhaitez exécuter.

```javascript
let maPromesse = new Promise((resolve, reject) => {
  // Code asynchrone ici
  if (/* condition de succès */) {
    resolve(valeur); // Résoudre la promesse avec une valeur
  } else {
    reject(new Error('Description de l\'erreur')); // Rejeter la promesse avec une instance d'Error
  }
});
```

Dans cet exemple, si la condition de succès est remplie, la promesse est résolue avec la `valeur` fournie. Sinon, elle est rejetée avec une nouvelle instance de `Error` contenant une description de l'erreur.

## Utiliser les promesses

Une fois qu'une promesse est créée, vous pouvez utiliser ses méthodes `.then()` et `.catch()` pour gérer ses états résolus et rejetés respectivement.

La méthode `.then()` prend deux fonctions en arguments : une pour gérer l'état résolu, et une optionnelle pour gérer l'état rejeté.

```javascript
maPromesse
  .then(
    valeur => {
      // Gérer la promesse résolue
      console.log(valeur);
    },
    erreur => {
      // Gérer la promesse rejetée (optionnel)
      console.error(erreur);
    }
  );
```

Vous pouvez également chaîner plusieurs appels à `.then()` pour gérer différentes étapes d'un processus asynchrone. Chaque appel à `.then()` renvoie une nouvelle promesse, ce qui permet de créer des chaînes d'opérations asynchrones.

La méthode `.catch()` est utilisée pour gérer les erreurs de manière centralisée dans une chaîne de promesses.

```javascript
maPromesse
  .then(valeur => {
    // Gérer la promesse résolue
    console.log(valeur);
    return autreFonctionAsynchrone(); // Renvoie une autre promesse
  })
  .catch(erreur => {
    // Gérer toutes les erreurs de la chaîne
    console.error(erreur);
  });
```

Dans cet exemple, si une erreur survient à n'importe quel endroit de la chaîne de promesses, elle sera gérée par le bloc `.catch()`.

## Gérer plusieurs promesses avec Promise.all() et Promise.race()

JavaScript fournit deux méthodes utilitaires pour gérer plusieurs promesses en parallèle : `Promise.all()` et `Promise.race()`.

La méthode `Promise.all()` attend que toutes les promesses passées en argument soient résolues, puis renvoie un tableau contenant leurs valeurs résolues dans le même ordre.

```javascript
Promise.all([promesse1, promesse2, promesse3])
  .then(valeurs => {
    // Toutes les promesses sont résolues
    console.log(valeurs); // [valeur1, valeur2, valeur3]
  })
  .catch(erreur => {
    // Au moins une promesse a été rejetée
    console.error(erreur);
  });
```

La méthode `Promise.race()` renvoie une promesse qui se résout ou se rejette dès que l'une des promesses passées en argument est résolue ou rejetée.

```javascript
Promise.race([promesse1, promesse2, promesse3])
  .then(valeur => {
    // La promesse la plus rapide est résolue
    console.log(valeur);
  })
  .catch(erreur => {
    // La promesse la plus rapide a été rejetée
    console.error(erreur);
  });
```

Ces méthodes sont utiles pour orchestrer des opérations asynchrones complexes impliquant plusieurs promesses.

## Utiliser les promesses avec AJAX

Les promesses sont particulièrement utiles pour gérer les requêtes AJAX. L'API Fetch, disponible dans les navigateurs modernes, renvoie une promesse qui se résout avec la réponse de la requête.

```javascript
fetch('/api/data')
  .then(response => response.json()) // Convertir la réponse en JSON
  .then(data => {
    // Gérer les données récupérées
    console.log(data);
  })
  .catch(erreur => {
    // Gérer les erreurs de la requête
    console.error(erreur);
  });
```

Dans cet exemple, nous utilisons `fetch()` pour envoyer une requête AJAX. La promesse renvoyée par `fetch()` est résolue avec la réponse de la requête. Nous utilisons ensuite `.then()` pour convertir la réponse en JSON, puis pour gérer les données récupérées. Si une erreur survient à n'importe quelle étape, elle sera gérée par le bloc `.catch()`.

## Utiliser les promesses avec React

Dans React, les promesses doivent être gérées dans les méthodes de cycle de vie appropriées, comme `componentDidMount()`. La résolution ou le rejet de la promesse doit mettre à jour l'état du composant, ce qui déclenchera un re-rendu pour afficher le résultat.

```javascript
class MonComposant extends React.Component {
  constructor(props) {
    super(props);
    this.state = { data: null, loading: true, erreur: null };
  }

  componentDidMount() {
    fetchData()
      .then(data => this.setState({ data, loading: false }))
      .catch(erreur => this.setState({ erreur, loading: false }));
  }

  render() {
    const { data, loading, erreur } = this.state;
    if (loading) {
      return <div>Chargement...</div>;
    }
    if (erreur) {
      return <div>Une erreur est survenue : {erreur.message}</div>;
    }
    return <div>{data}</div>;
  }
}
```

Dans cet exemple, la fonction `fetchData()` (non montrée) renvoie une promesse. Lorsque le composant est monté, nous appelons `fetchData()` et utilisons `.then()` pour mettre à jour l'état du composant avec les données récupérées et désactiver l'indicateur de chargement. Si une erreur survient, elle est gérée par le bloc `.catch()` en mettant à jour l'état avec l'erreur et en désactivant l'indicateur de chargement. Le rendu du composant affiche un message de chargement, une erreur ou les données selon l'état actuel.

## Utiliser les fonctions asynchrones (async/await)

Les fonctions asynchrones (async/await) sont une syntaxe plus récente introduite dans la norme ES2017 de JavaScript. Elles permettent d'écrire du code asynchrone d'une manière similaire au code synchrone, en utilisant les mots-clés `async` et `await`.

```javascript
async function fetchData() {
  try {
    const response = await fetch('/api/data');
    const data = await response.json();
    return data;
  } catch (erreur) {
    console.error(erreur);
    throw erreur; // Relancer l'erreur pour une gestion ultérieure
  }
}
```

Dans cet exemple, la fonction `fetchData` est marquée comme `async`, ce qui permet d'utiliser le mot-clé `await` à l'intérieur de la fonction. L'opération `fetch('/api/data')` renvoie une promesse, et `await` attend que cette promesse soit résolue avant de passer à l'étape suivante. Si une erreur survient, elle est gérée dans le bloc `catch`.

Les fonctions asynchrones offrent une syntaxe plus lisible et plus intuitive pour gérer le code asynchrone, mais sous le capot, elles reposent toujours sur les promesses. Elles sont désormais largement utilisées dans le développement JavaScript moderne, mais les promesses restent un concept fondamental à comprendre.

## Conclusion

Les promesses sont un outil puissant en JavaScript pour gérer le code asynchrone de manière plus structurée et lisible. Elles permettent d'éviter le fameux "callback hell" et offrent une syntaxe plus élégante grâce aux méthodes `.then()` et `.catch()`. Les promesses sont largement utilisées dans les bibliothèques et frameworks modernes comme React, facilitant ainsi la gestion des opérations asynchrones courantes comme les requêtes AJAX.

Avec les méthodes `Promise.all()` et `Promise.race()`, vous pouvez gérer plusieurs promesses en parallèle, offrant une grande flexibilité dans la coordination des opérations asynchrones complexes. Les fonctions asynchrones (async/await) apportent une syntaxe plus intuitive pour travailler avec les promesses, mais il est important de bien comprendre les concepts sous-jacents des promesses.

N'hésitez pas à pratiquer et à explorer davantage les promesses, ainsi que les fonctions asynchrones, pour maîtriser ces fonctionnalités essentielles de JavaScript !

## Ressources supplémentaires

- [Promesses - MDN Web Docs](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Objets_globaux/Promise)
- [Async/await - MDN Web Docs](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Instructions/async_function)
- [Comprendre les promesses en JavaScript - FreeCodeCamp](https://www.freecodecamp.org/news/comprendre-les-promesses-en-javascript/)
- [Promesses en JavaScript : une introduction - Eloquent JavaScript](https://eloquentjavascript.net/17_async.html)