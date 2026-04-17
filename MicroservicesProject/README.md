# MicroservicesProject

Application e-commerce en architecture microservices, construite avec Flask et Docker.

Le projet est composé de 4 services:

- `frontend`: interface web pour consulter les livres, s'inscrire, se connecter et passer commande.
- `user`: API de gestion des utilisateurs et de l'authentification.
- `book`: API du catalogue de livres.
- `order`: API de gestion du panier et des commandes.

Le frontend communique avec les autres services via HTTP. Le service `order` interroge aussi le service `user` pour valider l'utilisateur via sa `api_key`.

## Architecture

| Service | Rôle | Port |
| --- | --- | --- |
| `frontend-service` | Site web Flask | `5000` |
| `user-service` | API utilisateurs | `5001` |
| `book-service` | API livres | `5002` |
| `order-service` | API commandes | `5003` |

Chaque service stocke ses données dans une base SQLite locale au dossier `database/`.

## Prérequis

- Docker
- Docker Compose

## Lancer le projet avec Docker

Le stack complet se lance depuis le dossier `frontend/`, car le fichier de déploiement y référence les autres services.

```bash
cd frontend
docker compose -f docker-compose.deployment.yml up --build
```

Si votre version utilise l'ancien format, la commande équivalente est:

```bash
cd frontend
docker-compose -f docker-compose.deployment.yml up --build
```

Une fois les conteneurs démarrés, ouvrez l'application dans le navigateur:

- http://localhost:5000

## Arrêter le projet

```bash
cd frontend
docker compose -f docker-compose.deployment.yml down
```

## Fonctionnement général

1. Le frontend affiche la liste des livres depuis l'API `book`.
2. L'utilisateur peut créer un compte et se connecter via l'API `user`.
3. Une fois connecté, il peut ajouter des livres au panier.
4. Le service `order` crée ou met à jour la commande ouverte.
5. Le checkout ferme la commande en cours.

## Notes techniques

- Les conteneurs sont construits à partir de `python:3.13`.
- Les bases SQLite sont créées automatiquement au premier démarrage si elles n'existent pas.
- Les services exposent leurs ports sur la machine locale pour simplifier les tests.

## Structure du dépôt

- `frontend/`: interface web et client HTTP vers les microservices.
- `user/`: service utilisateurs.
- `book/`: service catalogue.
- `order/`: service commandes.

## Dépannage rapide

- Si un service ne répond pas, vérifiez que tous les conteneurs sont bien lancés.
- Si les données semblent vides, supprimez les volumes Docker du projet puis relancez le stack.
- Si vous modifiez le code, relancez avec `--build` pour reconstruire les images.