# Exercice technique

## Sujet

Créer un service Web, implantant diverses fonctionnalités, listées dans le mail accompagnant ce sujet.

Le service doit être écrit en Python, et s'exécuter sur un hôte Linux.
Sauf mention contraire, les données doivent être formattées en JSON.

Les spécifications peuvent être volontairement vagues, à vous de choisir!
Il est possible d'utiliser des dépendances.

Un client `clients.bin` est fourni, et permet de valider votre service.
**Il est très fortement recommandé de l'utiliser!**
Ce client ne vérifie pas toutes les propriétés attendues, seulement les plus visibles (à moins que quelque chose soit caché dedans, qui sait?).

Chaque fonctionnalité est indépendante, bien que présente dans le même service
web. Par exemple, l'identifiant utilisateur de F002 n'est pas lié à
l'identifiant de panier de F003.

## Fonctionnalités

### F001 - calculatrice

Le service doit exposer une route `/calculatrice`, prenant un paramètre d'URL `expr`.
Ce paramètre est une chaîne de caractères composée d'une valeur numérique, d'une opération, puis d'une autre valeur numérique.
L'objectif est de retourner le résultat de l'opération.

Par exemple:

```sh
$ curl http://localhost:8000/calculatrice?expr=5+%2B+8
13
$ curl http://localhost:8000/calculatrice?expr=5*8
40
```

Les opérations devant être supportées sont:
 * addition (`+`)
 * soustraction (`-`)
 * multiplication (`*`)
 * division (`/`)

Bonus:
 * support d'expressions plus complexes (par exemple `(4+8)/2`)

### F002 - authentification TPM

Le service doit exposer deux routes, permettant d'enregistrer un utilisateur, et
de l'authentifier. Les deux routes retournent `{"result":"ok"}` en cas de succès,
et une autre valeur, au choix de l'utilisateur en cas d'échec.

#### Enregistrement
Une requête de type `PUT` sur `/totp/register`, dont le corps a le format
suivant:

```json
{"secret": "XXXXX", "user": "YYYYY"}
```

Les paramètres ont les spécifications suivantes:

 * `secret`: chaîne de caractère entre 8 et 64 caractères alphanumériques ;
 * `user`: chaîne de caractère entre 4 et 16 caractères alphanumériques.

#### Authentification
Une requête de type `POST`, sur `/totp/auth`, dont le corps a le format suivant:

```json
{"password": "01234567"}
```

La requête possède également un en tête `X-User` contenant le nom de
l'utilisateur à authentifier.

#### Fonctionnement

Le service stocke les secrets associés au utilisateurs enregistrés par la route
`/totp/register` de façon chiffrée, au moyen du programme *GnuPG*.
**Il n'est pas permis d'utiliser une bibliothèque encapsulant les fonctionnalités de ce programme, le candidat doit l'appeler directement dans son code.**
Le secret doit être connu du service, il peut être "en dur", ou configurable.

Lorsque la route `/totp/auth` est appelée, le service doit:

 * récupérer l'heure UTC, et la formater de la façon suivante: `YYYYMMDD-HHMM`. On
   observe que les secondes ne sont pas présentes ;
 * récupérer le secret stocké correspondant à l'utilisateur `X-User`
   (après l'avoir déchiffré) ;
 * calculer le condensat SHA256 de la concaténation des deux chaînes (
   secret + temps) ;
 * rendre le condensat au format hexadécimal canonique (en minuscules), et en
   conserver les 16 premiers caractères (correspondant aux 8 premiers octets);
 * comparer ce résultat au paramètre `password` fourni par l'utilisateur.

Exemple:

```sh
$ curl -X PUT http://localhost:XXXX/totp/register \
    -d '{"secret":"AAAAAAAA", "user":"robert"}'
{"result": "ok"}
# il est 16:28 UTC, le 8 janvier 2022
$ curl -X POST http://localhost:XXXX/totp/auth \
    -H "X-User: robert"
    -d '{"password":"599e79061e8cc3b4"}'
{"result": "ok"}
# une minute plus tard
$ curl -X POST http://localhost:XXXX/totp/auth \
    -H "X-User: robert"
    -d '{"password":"9dc14e8ad9a9fbcd"}'
{"result": "ok"}
# une minute plus tard
$ curl -X POST http://localhost:XXXX/totp/auth \
    -H "X-User: robert"
    -d '{"password":"f57504571ad63a31"}'
{"result": "unauthorized"}
```

Bonus:

 * trouver une solution au problème de soumission d'un totp juste avant un
   changement de minute.

### F003 - commerce en ligne

Le service représente (de façon très schématique) un service de commerce en
ligne.  Il doit exposer les routes suivantes:
 * ajout de stock ;
 * modification du panier d'achat ;
 * visualisation du stock ;
 * confirmation de la commande.

Les identifiants de produits ou d'utilisateurs sont des valeurs numériques non
signées, représentables sur 32 bits.

Lorsque le service démarre, les stocks et paniers sont vides.

Toutes les données sont échangées au format JSON.  Sauf mention contraire, les
requêtes doivent retourner `{"result": "ok"}` en cas de succès, et un message
arbitraire en cas d'erreur.

#### Ajout de stock
Une requête de type `PUT`, sur `/shop/stock`, dont le corps a le format suivant:

```json
[{"id": 123, "amount": 4}, {"id": 64, "amount": 1}]
```

Cette requête indique que `4` exemplaires du produit `123` ont été ajoutés au
stock, ainsi qu'un exemplaire du produit `64`. Le même `id` peut être présent
plusieurs fois.

#### Modification du panier

Une requête de type `POST`, sur `/shop/basket`, dont le corps a le format
suivant:

```json
{"id": 214124, "basket": [{"id": 123, "amount": 5}, {"id": 64, "amount": 2}]}
```

Ce message signifie que le panier `214124` contient 5 exemplaires de l'article
`123` et 2 exemplaires de l'article `64`. Si cette requête est utilisée
plusieurs fois pour le même sur le même identifiant de panier, son contenu est
remplacé.

Le fait de mettre des objets dans un panier ne modifie pas le stock.
Le stock ne diminue que lorsque la commande est confirmée (voir plus bas).

Les réponses possibles sont:

 * `{"result": "ok"}` lorsque la modification est acceptée ;
 * `{"result": "oos"}` lorsque le stock n'est pas suffisant pour honorer une
 commande avec cette quantité de produits.


#### Visualisation du stock

Une requête de type `GET`, sur `/shop/stock`.

La réponse doit avoir le format suivant:

```json
[{"id": 123, "amount": 5}, {"id": 64, "amount": 2}]
```

Indiquant la quantité d'objets en stock. Le même `id` ne peut être présent
qu'une seule fois.

#### Confirmation de la commande

Une requête de type `POST`, sur `/shop/checkout`, avec le corps suivant:

```json
{"id": 214124}
```

La réponse doit avoir le format suivant:

```json
[{"id": 4, "amount": 8}]
```

Ce qui signifie que la commande est prise en compte, et que le panier contenait
8 articles de type `4`.

Cette requête ne doit jamais échouer, c'est à dire qu'il doit toujours être
possible de confirmer un panier.

Lorsque la requête est validée, le stock doit refléter le fait que les articles
ne sont plus disponibles.

#### Bonus

En bonus, les données peuvent être persistantes, c'est à dire que le service
conserve ses données même lorsqu'il est redémarré.

### F004 - application vulnérable

L'archive contient une application ayant diverses failles de sécurité. Il est
demandé de les trouver, et de les corriger. N'hésitez pas à commenter les
correction pour expliquer votre démarche. Contrairement aux autres épreuves,
vous devrez fournir un fichier patch (tel qu'obtenu avec l'outil patch, la
commande `git diff` ou la commande `git format-patch`) ainsi que le code du serveur patché.

## Rendu attendu

Une archive tgz qui contient:
  * le code source python du service répondant à l'exercice. Le service sera
    testé avec `gunicorn` ou `uvicorn`, et des instructions décrivant ce
    scénario seront appréciées (bien que non obligatoires)
  * un fichier texte `README.txt` qui contient les informations suivantes sur le
    programme: sa description, les instructions pour son utilisation, son
    déploiement en production de manière sécurisé, ses tests et toute autre
    information pertinente
  * un fichier texte `REPORT.txt` qui contient les informations sur la
    résolution de cet exercice, notamment le temps nécessaire (à indiquer
    globalement, et pas par tâche), les ressources utilisées, les pistes suivies
    (bonnes ou pas), l'approche retenue, les difficultés rencontrées, etc.
  * un dossier test contenant le nécessaire pour s'assurer du bon fonctionnement
    du service
  * plus tout autre fichier ou ressource jugée importante
  * pour F004, les fichiers de l'application modifiés, avec éventuellement un
    rapport décrivant les vulnérabilités corrigées

Conseil: chaque exercice est conçu pour se résoudre relativement rapidement
(environ 2h) par un développeur familier de la création d'application Web en
Python.

## Critères d'évaluation

Par ordre d'importance:

 * atteinte de l'objectif
 * respect des consignes
 * qualité du code (propre, clair, concis, documenté, ...)
 * performances du code
 * qualité du rendu des résultats, lorsque applicable (clair, lisible, joli)
 * ... et, en dernier, les points bonus
