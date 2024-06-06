# Démarrer un thread dans Django

Dans le développement web avec Django, il peut être nécessaire d'exécuter certaines tâches en arrière-plan de manière asynchrone. C'est là qu'interviennent les threads. Un thread est un fil d'exécution léger au sein d'un processus, permettant d'exécuter plusieurs tâches en parallèle. Dans cet article, nous explorons différentes façons de démarrer un thread dans Django, adaptées aux débutants.

## Utilisation de la classe threading.Thread de Python

L'approche la plus simple consiste à sous-classer la classe threading.Thread et à remplacer la méthode run() par la fonctionalité souhaitée. Cependant, cette méthode n'est pas recommandée pour les sites web publics en raison des risques potentiels d'épuisement des ressources en cas de forte charge ou d'attaques par déni de service.

Exemple de code :

```python
import threading

class MonThread(threading.Thread):
    def run(self):
        # Code à exécuter dans le thread d'arrière-plan
        print("Exécution du thread d'arrière-plan")
```

## Thread d'arrière-plan avec CherryPy

Pour les applications Django hébergées avec le serveur WSGI CherryPy, un thread d'arrière-plan peut être démarré et maintenu au sein de l'application. Cette approche implique la création d'un plugin CherryPy personnalisé et l'utilisation de la méthode engine.subscribe() pour démarrer le thread.

Exemple de code :

```python
import cherrypy
import threading

class ThreadArriereplan(cherrypy.process.plugins.SimplePlugin):
    def __init__(self, bus):
        self.thread = None

    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        # Code à exécuter dans le thread d'arrière-plan
        print("Exécution du thread d'arrière-plan")

    def stop(self):
        if self.thread:
            self.thread.join()
```

## Démarrage du thread dans la configuration de l'application Django (AppConfig)

Une autre approche consiste à démarrer un nouveau thread dans la méthode ready() de la classe AppConfig de l'application Django (définie dans le fichier apps.py). Cette méthode est exécutée au démarrage du serveur, permettant au thread de s'exécuter en arrière-plan pendant toute la durée de vie de l'application. Pour plus de détails sur la programmation asynchrone en Python, vous pouvez consulter notre article [**Asynchronous Programming in Python**](https://tim-tek.com/async-python).

Exemple de code :

```python
from django.apps import AppConfig
import threading

class ConfigAppMon(AppConfig):
    name = 'mon_app'

    def ready(self):
        thread = threading.Thread(target=self.executer_tache_arriere_plan)
        thread.start()

    def executer_tache_arriere_plan(self):
        # Code à exécuter dans le thread d'arrière-plan
        print("Exécution du thread d'arrière-plan")
```

## Compréhension des processus du serveur Django

Il est important de noter que la commande Django runserver démarre deux processus : le processus principal et un processus de rechargement automatique. Lors du débogage des threads, il est essentiel de comprendre que les threads peuvent redémarrer lorsque des modifications de code sont détectées par le processus de rechargement automatique.

## Recommandation pour les tâches longues

Pour les tâches de longue durée ou les opérations susceptibles de bloquer le processus principal du serveur Django, il est fortement recommandé d'utiliser un système de file d'attente de tâches comme Celery ou RabbitMQ au lieu de lancer directement des threads à partir du processus du serveur Django. Les files d'attente de tâches permettent de déléguer les tâches chronophages à des processus de travail séparés, garantissant que le serveur principal reste réactif et évitant tout risque d'épuisement des ressources. Pour en savoir plus sur la programmation asynchrone, vous pouvez consulter notre article [**Comprehending Promises in JavaScript**](https://tim-tek.com/javascript-promises).

En résumé, bien qu'il soit possible de démarrer des threads d'arrière-plan dans Django, il est crucial de prendre en compte les risques potentiels d'épuisement des ressources et la pertinence de l'approche pour le cas d'utilisation spécifique. Pour les tâches de longue durée, l'utilisation d'un système de file d'attente de tâches est fortement recommandée afin de maintenir la réactivité, l'évolutivité et la stabilité du serveur.

## Lectures complémentaires

- [Documentation officielle de Python - Module threading](https://docs.python.org/3/library/threading.html)
- [Documentation Django - Prise en charge asynchrone](https://docs.djangoproject.com/en/5.0/topics/async/)
- [Réponse Stack Overflow : "Comment démarrer un thread d'arrière-plan lorsque le serveur Django est en cours d'exécution ?"](https://stackoverflow.com/questions/59541954/how-to-start-a-background-thread-when-django-server-is-up)