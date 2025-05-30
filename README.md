
# 📦 Mini WebApp IA (Docker + Flask + MongoDB)

Ce projet est une **application web minimaliste en microservices** construite avec Docker. Elle simule un système d’**analyse textuelle** à l’aide d’un microservice d’IA fictif, et stocke les résultats dans une base de données MongoDB.

---

## 🧱 Architecture du projet

```
.
├── flask-app/         # WebApp Flask (formulaire HTML)
├── ia-service/        # Microservice IA (prédiction simulée)
├── data/              # Dossier monté (upload/local)
├── docker-compose.yml
```

---

## ⚙️ Services Docker

| Service       | Rôle                                 | Port exposé | Réseau     |
|---------------|--------------------------------------|-------------|------------|
| `flask-app`   | WebApp Flask (UI + envoi données)    | 5002        | `frontend-net`, `backend-net` |
| `ia-service`  | Microservice Flask (retourne une prédiction textuelle simulée) | ❌ | `frontend-net` |
| `mongo-db`    | Base de données MongoDB              | ❌          | `backend-net` |

---

## 🔐 Réseaux & sécurité

- `frontend-net` : relie `flask-app` et `ia-service`
- `backend-net` : relie `flask-app` et `mongo-db`
- Les services **`ia-service`** et **`mongo-db`** ne sont **pas exposés** à l’extérieur → **réseaux privés**

---

## 💾 Volume

```yaml
volumes:
  - mongo-data:/data/db
```

- Volume **nommé Docker** : `mongo-data`
- Utilisé pour persister les données de MongoDB
- Géré automatiquement par Docker (`docker volume ls`)

---

## 🚀 Lancer l'application

```bash
docker-compose up --build
```

Puis ouvre dans ton navigateur :
👉 http://localhost:5002

---

## 🧪 Utilisation

1. Saisis un texte dans le formulaire
2. Clique sur **Envoyer**
3. Le microservice IA retourne une prédiction (texte inversé pour simuler une IA)
4. Le résultat est affiché et enregistré dans MongoDB

---

## 🧰 Inspecter les prédictions dans MongoDB

```bash
docker exec -it projet-mongo-db-1 mongosh
```

```js
use prediction_db
db.predictions.find().pretty()
```

---

## ✅ Exigences respectées

| Critère                       | Statut |
|------------------------------|--------|
| 3 conteneurs                 | ✅     |
| 1 volume                     | ✅     |
| 2 réseaux                    | ✅     |
| Réseaux privés               | ✅     |
| Base de données fonctionnelle| ✅     |

---

## 📎 À propos

Ce projet a été conçu à des fins pédagogiques pour illustrer :
- l’isolation des services via des **réseaux Docker**
- l’architecture **multi-tiers** simple avec **Flask + IA + DB**
- les bonnes pratiques de **séparation des responsabilités** en microservices
