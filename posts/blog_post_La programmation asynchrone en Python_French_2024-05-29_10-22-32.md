# La programmation asynchrone en Python avec asyncio

Dans le monde de la programmation Python, l'exécution asynchrone de tâches est devenue un concept clé pour améliorer les performances et l'utilisation efficace des ressources système. Le module `asyncio` offre un cadre robuste pour l'écriture de code asynchrone à l'aide de coroutines et d'une boucle d'événements. Dans cet article de blog, nous explorerons les concepts fondamentaux et les détails de la mise en œuvre de la programmation asynchrone avec `asyncio`.

## Qu'est-ce que la programmation asynchrone ?

La programmation asynchrone permet l'exécution concurrente de tâches, ce qui signifie que plusieurs tâches peuvent s'exécuter en même temps, sans avoir à attendre que l'une d'entre elles soit terminée. Cette approche diffère de la programmation synchrone, dans laquelle les tâches s'exécutent de manière séquentielle, une après l'autre.

Dans le contexte de Python, le module `asyncio` fournit un moyen élégant d'implémenter la programmation asynchrone à l'aide de coroutines et d'une boucle d'événements.

## Les concepts clés de `asyncio`

### Coroutines

Les coroutines sont des fonctions légères qui peuvent être suspendues et reprises, permettant à d'autres tâches de s'exécuter pendant la période de suspension. Dans `asyncio`, les coroutines sont définies à l'aide des mots-clés `async` et `await`.

Voici un exemple simple de coroutine :

```python
import asyncio

async def hello_world():
    print("Hello, World!")
    await asyncio.sleep(1)  # Simuler une opération de blocage
    print("Hello again!")
```

Dans cet exemple, la fonction `hello_world` est une coroutine définie avec le mot-clé `async`. Elle imprime un message, simule une opération de blocage en attendant pendant une seconde grâce à `await asyncio.sleep(1)`, puis imprime un autre message.

### Boucle d'événements

La boucle d'événements (event loop) est le composant central de `asyncio` qui gère l'exécution des coroutines et traite les opérations d'entrée/sortie (E/S). Elle vérifie continuellement les tâches disponibles et les exécute de manière concurrente.

Vous pouvez accéder à la boucle d'événements par défaut avec la fonction `asyncio.get_event_loop()`.

### Tâches

Les tâches représentent des unités de travail individuelles qui sont planifiées et exécutées par la boucle d'événements. Elles sont créées en encapsulant des coroutines avec la fonction `asyncio.create_task` ou `loop.create_task`.

Voici un exemple de création et d'exécution d'une tâche :

```python
import asyncio

async def hello_world():
    print("Hello, World!")
    await asyncio.sleep(1)
    print("Hello again!")

loop = asyncio.get_event_loop()
task = loop.create_task(hello_world())
loop.run_until_complete(task)
loop.close()
```

Dans cet exemple, nous créons une tâche en encapsulant la coroutine `hello_world` avec `loop.create_task(hello_world())`. Ensuite, nous exécutons la tâche en appelant `loop.run_until_complete(task)`, ce qui fait que la boucle d'événements exécute la coroutine jusqu'à ce qu'elle soit terminée.

### Concurrence et opérations de blocage

La programmation asynchrone avec `asyncio` permet l'exécution concurrente de tâches sans le surcoût de création de threads ou de processus séparés. Cela est rendu possible en suspendant les coroutines pendant les opérations de blocage (par exemple, les opérations d'E/S, les requêtes réseau) et en permettant à la boucle d'événements de passer à d'autres tâches.

Voici un exemple illustrant la concurrence avec `asyncio` :

```python
import asyncio
import time

async def task(name, delay):
    start = time.time()
    print(f"[{name}] Début de la tâche...")
    await asyncio.sleep(delay)
    end = time.time()
    print(f"[{name}] Tâche terminée après {end - start:.2f} secondes.")

async def main():
    await asyncio.gather(
        task("Tâche 1", 2),
        task("Tâche 2", 1),
        task("Tâche 3", 3)
    )

asyncio.run(main())
```

Dans cet exemple, nous définissons une coroutine `task` qui simule une tâche en attendant pendant un certain délai. Ensuite, nous utilisons la fonction `asyncio.gather` pour exécuter plusieurs tâches simultanément. La boucle d'événements gère l'exécution concurrente de ces tâches, en les suspendant pendant les opérations de blocage (`await asyncio.sleep(delay)`) et en passant à d'autres tâches disponibles.

## Exemples pratiques

### Exemple 1 : Programmation synchrone vs. asynchrone

Voyons d'abord la différence entre la programmation synchrone (Python régulier) et la programmation asynchrone avec `asyncio`.

**Programmation synchrone :**

```python
import time

def sleep():
    print(f'Time: {time.time() - start:.2f}')
    time.sleep(1)

def sum(name, numbers):
    total = 0
    for number in numbers:
        print(f'Task {name}: Computing {total}+{number}')
        sleep()
        total += number
    print(f'Task {name}: Sum = {total}\n')

start = time.time()
tasks = [sum("A", [1, 2]), sum("B", [1, 2, 3])]
end = time.time()
print(f'Time: {end-start:.2f} sec')
```

Dans cet exemple synchrone, les tâches `sum("A", [1, 2])` et `sum("B", [1, 2, 3])` s'exécutent séquentiellement, chacune bloquant jusqu'à ce qu'elle soit terminée. Cela signifie que la seconde tâche ne commencera pas avant que la première ne soit terminée.

**Programmation asynchrone (utilisation incorrecte) :**

```python
import asyncio
import time

async def sleep():
    print(f'Time: {time.time() - start:.2f}')
    time.sleep(1)

async def sum(name, numbers):
    total = 0
    for number in numbers:
        print(f'Task {name}: Computing {total}+{number}')
        await sleep()
        total += number
    print(f'Task {name}: Sum = {total}\n')

start = time.time()
loop = asyncio.get_event_loop()
tasks = [loop.create_task(sum("A", [1, 2])), loop.create_task(sum("B", [1, 2, 3]))]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
end = time.time()
print(f'Time: {end-start:.2f} sec')
```

Dans cet exemple, bien que nous utilisions `async` et `await`, la fonction `time.sleep(1)` bloque encore l'ensemble de la tâche, empêchant la boucle d'événements de passer à d'autres tâches pendant la période de sommeil.

**Programmation asynchrone (utilisation correcte) :**

```python
import asyncio
import time

async def sleep():
    print(f'Time: {time.time() - start:.2f}')
    await asyncio.sleep(1)

async def sum(name, numbers):
    total = 0
    for number in numbers:
        print(f'Task {name}: Computing {total}+{number}')
        await sleep()
        total += number
    print(f'Task {name}: Sum = {total}\n')

start = time.time()
loop = asyncio.get_event_loop()
tasks = [loop.create_task(sum("A", [1, 2])), loop.create_task(sum("B", [1, 2, 3]))]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
end = time.time()
print(f'Time: {end-start:.2f} sec')
```

Dans cet exemple, nous remplaçons `time.sleep(1)` par `await asyncio.sleep(1)`, ce qui permet à la boucle d'événements de passer à d'autres tâches pendant la période de sommeil, résultant en une meilleure performance.

### Exemple 2 : Application asynchrone simple

Voici un exemple d'application asynchrone simple utilisant des coroutines, des tâches et la boucle d'événements :

```python
import asyncio

result2 = 0

async def compute(x, y):
    print(f"Compute {x} + {y} ...")
    await asyncio.sleep(1.0)
    result2 = x * y
    return x + y

async def print_sum(x, y):
    result = await compute(x, y)
    print(f"{x} + {y} = {result}")

async def dosomethingelse():
    print("I've got a lovely bunch of coconuts")

loop = asyncio.get_event_loop()
tasks = [print_sum(1, 2), dosomethingelse(), compute(2, 4)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
print(result2)
```

Dans cet exemple, la coroutine `compute` simule un calcul de longue durée en attendant pendant 1 seconde. La coroutine `print_sum` appelle `compute` et imprime le résultat. La coroutine `dosomethingelse` représente une autre tâche qui peut s'exécuter en même temps que les autres.

La boucle d'événements planifie et exécute ces tâches, leur permettant de s'exécuter de manière concurrente et de basculer l'exécution pendant la période de sommeil.

## Conclusion

La programmation asynchrone avec le module `asyncio` de Python offre un moyen puissant et efficace de gérer les tâches concurrentes sans le surcoût de la création de threads ou de processus séparés. En tirant parti des coroutines, des tâches et de la boucle d'événements, `asyncio` permet une exécution concurrente et une utilisation efficace des ressources, particulièrement dans les applications liées aux opérations d'entrée/sortie.

Les exemples fournis dans cet article illustrent les concepts fondamentaux et les détails de la mise en œuvre, facilitant ainsi la compréhension et l'application de la programmation asynchrone en Python avec `asyncio`.