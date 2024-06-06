# Comment créer un bot Discord

Vous souhaitez créer un bot Discord, mais vous ne savez pas par où commencer ? Ce guide détaillé est fait pour vous ! Nous allons vous expliquer, pas à pas, comment créer un bot Discord en utilisant la bibliothèque `discord.js` pour Node.js. Nous inclurons des exemples de code pratiques pour que vous puissiez suivre facilement. Mais avant de commencer, qu'est-ce qu'un bot Discord ? Un bot Discord est une application automatisée qui peut interagir avec les utilisateurs et effectuer diverses tâches sur un serveur Discord, comme répondre à des messages, modérer les discussions, et bien plus encore.

## 1. Préparer votre environnement

Avant de commencer, assurez-vous d'avoir les éléments suivants :

1. [Node.js](https://nodejs.org/) installé sur votre machine (version recommandée : 14.x ou supérieure).
2. Un compte Discord.
3. Un éditeur de code (comme [Visual Studio Code](https://code.visualstudio.com/)).

## 2. Créer une application Discord

Pour que votre bot puisse interagir avec Discord, il doit être enregistré en tant qu'application. Voici comment faire :

1. Rendez-vous sur le [Discord Developer Portal](https://discord.com/developers/applications).
2. Cliquez sur « Nouvelle application ».
3. Donnez un nom à votre application et cliquez sur « Créer ».
4. Dans le menu de gauche, allez dans « Bot » et cliquez sur « Ajouter un bot ».
5. Confirmez en cliquant sur « Oui, faites-le ! ».

## 3. Configurer votre bot

Vous devez maintenant récupérer le jeton de votre bot pour l'authentifier. Ce jeton est comme une clé secrète qui permet à votre bot de se connecter à Discord. **Ne partagez jamais ce jeton publiquement !**

1. Toujours dans le menu « Bot », cliquez sur « Copier » sous « TOKEN ».
2. Gardez ce token en lieu sûr, vous en aurez besoin pour coder votre bot.

## 4. Installer discord.js

Ouvrez votre terminal et créez un nouveau dossier pour votre projet. Ensuite, initialisez un projet Node.js et installez `discord.js` :

```bash
mkdir my-discord-bot
cd my-discord-bot
npm init -y
npm install discord.js
```

La commande `npm init -y` crée un fichier `package.json` par défaut, nécessaire pour gérer les dépendances de votre projet. Pour en savoir plus sur la gestion des promesses en JavaScript, consultez notre article sur [Comprehending Promises in JavaScript](https://tim-tek.com/javascript-promises).

## 5. Écrire le code de base

Créez un fichier `index.js` dans votre dossier de projet et ouvrez-le dans votre éditeur de code. Ajoutez le code suivant pour configurer votre bot :

```javascript
const { Client, Intents } = require("discord.js");
const client = new Client({
  intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES],
});

client.once("ready", () => {
  console.log("Bot is online!");
});

client.login("YOUR_BOT_TOKEN");
```

Remplacez `'YOUR_BOT_TOKEN'` par le token de votre bot. Ce code initialise un nouveau client Discord et se connecte à Discord avec le token de votre bot.

## 6. Ajouter des commandes

Ajoutons une commande simple pour vérifier que notre bot fonctionne. Modifiez votre `index.js` pour inclure le code suivant :

```javascript
client.on("messageCreate", (message) => {
  if (message.content === "!ping") {
    message.channel.send("Pong!");
  }
});
```

Ce code écoute les messages et répond par "Pong!" lorsque quelqu'un tape `!ping`.

## 7. Tester votre bot

Pour tester votre bot, vous devez l'inviter sur un serveur Discord.

1. Retournez sur le [Discord Developer Portal](https://discord.com/developers/applications), sélectionnez votre application, et allez dans « OAuth2 ».
2. Dans « OAuth2 URL Generator », cochez « bot » dans les scopes et sélectionnez les permissions dont votre bot aura besoin (par exemple, envoyer des messages, lire les messages, etc.).
3. Copiez l'URL générée et ouvrez-la dans votre navigateur pour inviter le bot sur votre serveur.

## 8. Héberger votre bot

Pour que votre bot soit toujours en ligne, vous devrez l'héberger. Une solution simple et gratuite est d'utiliser [Heroku](https://dashboard.heroku.com/).

1. Créez un compte Heroku et installez l'[interface en ligne de commande Heroku](https://devcenter.heroku.com/articles/heroku-cli).
2. Dans votre terminal, connectez-vous à Heroku :

```bash
heroku login
```

3. Créez un nouveau projet Heroku :

```bash
heroku create my-discord-bot
```

4. Poussez votre code vers Heroku :

```bash
git init
heroku git:remote -a my-discord-bot
git add .
git commit -m "Initial commit"
git push heroku master
```

Votre bot devrait maintenant être en ligne 24/7 !

## 9. Aller plus loin

Pour ajouter des fonctionnalités plus avancées à votre bot, comme répondre à des commandes spécifiques ou interagir avec des API externes, vous pouvez consulter les ressources supplémentaires ci-dessous. Si vous êtes intéressé par la programmation asynchrone, n'hésitez pas à lire notre article sur [Asynchronous Programming in Python](https://tim-tek.com/async-python).

## Further Reading

- [Discord Developer Portal — Getting Started](https://discord.com/developers/docs/quick-start/getting-started)
- [Grafikart — Tutoriel vidéo NodeJS : Créer un bot Discord](https://grafikart.fr/tutoriels/bot-discordjs-892)
- [IONOS — Créer un bot Discord : étape par étape](https://www.ionos.fr/digitalguide/serveur/know-how/creer-un-bot-discord/)

Avec ces informations, vous êtes prêt à créer et personnaliser votre propre bot Discord. Amusez-vous bien et bonne chance !
