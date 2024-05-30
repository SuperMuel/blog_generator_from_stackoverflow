# Comprendre les promesses en JavaScript

Les promesses en JavaScript sont un moyen de gérer les opérations asynchrones de manière élégante et structurée. Elles représentent l'achèvement éventuel ou l'échec d'une opération asynchrone et sa valeur résultante. Dans ce billet de blog détaillé, nous allons explorer les concepts clés des promesses et leur utilisation correcte.

## La métaphore de la promesse

Une métaphore utile pour comprendre les promesses est de les comparer à commander une pizza dans un restaurant. Lorsque vous passez une commande (créez une promesse), on vous donne un vibreur (l'objet promesse) qui vous avertira lorsque la pizza sera prête (l'opération asynchrone sera terminée).

La fonction passée au constructeur Promise est comme le cuisinier qui prépare la pizza :

```js
function cuisinierPizza(resoudre, rejeter) {
    let bool = false; 

    if (bool) {
        resoudre('La pizza est prête !'); // Appeler resoudre si la pizza est prête
    } else {
        rejeter('Désolé, le four est en panne !'); // Appeler rejeter s'il y a eu une erreur
    }
}

let p = new Promise(cuisinierPizza);
```

Les fonctions `resoudre` et `rejeter` sont utilisées par le cuisinier (opération asynchrone) pour signaler si la pizza a été préparée avec succès (`resoudre`) ou s'il y a eu une erreur (`rejeter`).

Vous fournissez des gestionnaires pour ces cas en utilisant `.then()` et `.catch()` :

```js
p.then(msg => console.log(`Génial, je peux manger maintenant : ${msg}`))
 .catch(msg => console.log(`Oh non, je resterai affamé : ${msg}`));
```

Le gestionnaire `.then()` est appelé avec la valeur passée à `resoudre()`, comme recevoir la pizza prête. Le gestionnaire `.catch()` est appelé avec la valeur passée à `rejeter()`, comme être notifié que le four est en panne.

## Comprendre les promesses en coulisses

Les promesses impliquent une fonction "exécutrice" qui est exécutée immédiatement et de manière synchrone lors de la création de la promesse. Cet exécuteur démarre généralement une opération asynchrone et appelle `resoudre` ou `rejeter` lorsqu'elle est terminée.

Les promesses ont trois états : en attente, résolue et rejetée. Les transitions d'état sont unidirectionnelles (en attente -> résolue, ou en attente -> rejetée).

Chaque promesse a une méthode `.then()` qui permet le chaînage. Lorsque `.then()` est appelé, une nouvelle promesse est créée et renvoyée. Les fonctions passées à `.then()` sont toujours invoquées de manière asynchrone dans la file d'attente des microtâches.

Si une promesse est résolue avec une autre promesse, les deux chaînes sont jointes, et la promesse extérieure prend l'état de la promesse intérieure.

Voici une implémentation simplifiée de la classe Promise :

```js
function Promise(executeur) {
  let statut = "en attente", valeur, fileQ = [];

  const then = onResolu => {
    let resolveur;
    const nouvellePromesse = new Promise(resoudre => resolveur = resoudre);
    fileQ.push((...args) => resolveur(onResolu(...args)));
    return nouvellePromesse;
  }

  const resoudre = resultat => resultat?.then ? resultat.then(accomplir) : accomplir(resultat);
  const accomplir = resultat => (statut = "resolue", valeur = resultat, executerThens(valeur));
  const executerThens = valeur => queueMicrotask(() => fileQ.forEach(el => el(valeur)));

  executeur(resoudre);

  return { then, get statut() { return statut }, get valeur() { return valeur } };
}
```

## Utilisation correcte des promesses

Lors de l'utilisation des promesses, il est important de comprendre la syntaxe pour passer des fonctions de rappel ou les exécuter immédiatement. Avec `setTimeout` et `promise.then`, les fonctions doivent être passées, pas invoquées.

```js
// Correct : Passer une référence de fonction
setTimeout(foo, 3000); 
promise.then(foo);

// Incorrect : Invoquer la fonction
setTimeout(foo(), 3000); // foo() est invoqué immédiatement
promise.then(foo()); // foo() est invoqué immédiatement
```

Un autre problème courant est une promesse non résolue, où ni `resoudre` ni `rejeter` n'est appelé, ce qui fait que les gestionnaires `.then` ne s'exécutent jamais. Pour résoudre ce problème, la promesse doit être résolue après l'achèvement de l'opération asynchrone.

```js
function testPromesse() {
  let promesse = new Promise(function(resoudre, rejeter) {
    setTimeout(function() {
      foo(); 
      resoudre(); // Résoudre la promesse après l'appel de foo()
    }, 3000);
  });
  promesse.then(bar);
}
```

De plus, bien qu'attendre une promesse mette en pause l'exécution de la fonction asynchrone, cela ne bloque pas la boucle d'événements ni n'affecte les autres tâches.

## Gestion des exceptions de promesse

Il est essentiel de gérer correctement les exceptions de promesse. Les rejets de promesse non gérés peuvent entraîner des défaillances du système. L'approche recommandée consiste à utiliser `.catch()` pour gérer les erreurs ou à les laisser remonter.

```js
appelAsyncDB()
  .catch(err => console.error(err)) // Gérer l'erreur
  .then(() => apres()); // Continuer avec l'opération suivante

// Ou laisser les erreurs remonter
async function faireQuelqueChose() {
  try {
    await avant();
    await appelAsyncDB();
    await apres();
  } catch (err) {
    // Gérer l'erreur
  }
}
```

En résumé, les promesses offrent un moyen de gérer les opérations asynchrones en JavaScript, proposant une approche plus structurée que les callbacks. Comprendre les concepts clés, l'utilisation correcte et la gestion des erreurs est crucial pour écrire du code asynchrone robuste et maintenable.