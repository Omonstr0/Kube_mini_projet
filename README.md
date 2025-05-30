
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

## 🔒 Preuve que les réseaux sont privés

### 1. Aucun port exposé pour les services internes

Dans `docker-compose.yml`, seuls les ports du service `flask-app` sont exposés :

```yaml
  ia-service:
    networks:
      - frontend-net
    # aucun port exposé → inaccessible depuis l'extérieur

  mongo-db:
    networks:
      - backend-net
    # aucun port exposé → inaccessible depuis l'extérieur
```

---

### 2. Résultat de `docker ps`

Seul `flask-app` expose un port :

```bash
$ docker ps

CONTAINER ID   IMAGE             PORTS
...            projet-flask-app  0.0.0.0:5002->5000/tcp
...            projet-ia-service  <aucun port exposé>
...            projet-mongo-db   <aucun port exposé>
```

➡️ `ia-service` et `mongo-db` ne sont **pas accessibles depuis l’extérieur**.

---

### 3. `docker network inspect`

Chaque réseau Docker n'inclut que les services autorisés. Exemple :

```bash
docker network inspect Kube_mini_projet
```

Retour partiel :

```json
"Containers": {
  "projet-flask-app-1": {...},
  "projet-ia-service-1": {...}
}
```

➡️ Seuls les conteneurs nécessaires sont connectés au réseau.

---

### 4. Tentative d'accès depuis l'extérieur échoue

```bash
curl http://localhost:5002
```

Résultat :

```
curl: (7) Failed to connect to localhost port 5002: Connection refused
```

➡️ Confirmation que `ia-service` est **isolé du réseau public**.

---

### 5. Communication interne prouvée dans le code

Dans `flask-app/app.py` :

```python
requests.post('http://ia-service:5000/predict')
```

➡️ `flask-app` communique avec `ia-service` uniquement via le **réseau Docker privé** (`frontend-net`).

---

🟢 Ces éléments démontrent que l’architecture respecte les bonnes pratiques de **réseaux privés et sécurisés en environnement Docker**.


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
