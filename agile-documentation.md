# Agile Documentation

## 1. Pilotage du projet avec Scrum

Dans le cadre du développement de notre système de recommandation de films basé sur les principes du DataOps et du MLOps, nous avons adopté la méthodologie agile Scrum afin d'organiser efficacement le travail de l'équipe et de garantir une livraison progressive des fonctionnalités.

### 1.1 Équipe et Rôles
L'équipe est composée de huit membres répartis selon quatre rôles techniques :
- **Product Owner (1)** : Définition des besoins métier, priorisation du backlog, validation des fonctionnalités développées. (Hamza RBIB)
- **Scrum Master (1)** : Organisation des sprints, suivi de l'avancement, suppression des obstacles. (Imrane TAYA)
- **Data Engineers (2)** : Ingestion des données, création des pipelines DataOps, transformation et validation des données. (Abderrahmane Hassani, Hajar EL KHALIDI)
- **ML Engineers (2)** : Développement du modèle de recommandation, suivi des expériences MLflow, déploiement du modèle. (Youness Zouhairi, Douaa Bounadar)
- **Data Analysts (2)** : Analyse exploratoire des données, contrôle qualité, création des rapports et indicateurs de suivi. (Abdelkarim Moussaoui, Nohaila Ichou)

### 1.2 Phases Principales du Projet
Le projet est divisé en plusieurs phases principales :
- Ingestion et stockage des données avec dlt et DuckDB.
- Transformation et validation des données avec dbt.
- Développement du modèle de recommandation.
- Suivi des expériences avec MLflow.
- Déploiement du modèle via FastAPI.
- Mise en place de l'intégration continue et du monitoring.

---

## 2. Planification des Sprints

Le projet est divisé en trois sprints successifs. Chaque sprint se termine par la livraison d'un incrément fonctionnel validé lors d'une réunion de revue de sprint. Cette planification permet de répartir les fonctionnalités sur plusieurs itérations tout en respectant les dépendances entre les tâches DataOps et MLOps.

### Sprint 1 : DataOps et préparation des données (Estimation : 23/06 au 26/06)
L'objectif de ce sprint est de mettre en place l'infrastructure de données nécessaire à l'entraînement du modèle de recommandation.
- **Fonctionnalités réalisées :**
  - Ingestion automatique des données avec dlt.
  - Stockage des données dans DuckDB local.
  - Transformation des données avec dbt.
  - Création des modèles analytiques.
  - Orchestration globale via Dagster.
  - Mise en place des tests de qualité des données.
- **Contributeurs :** Data Engineers, Data Analysts.
- **Livrables :** Pipeline DataOps entièrement fonctionnel, données propres et prêtes pour l'apprentissage automatique.

### Sprint 2 : Développement du modèle de recommandation (Estimation : 26/06 au 30/06)
L'objectif de ce sprint est de construire et d'évaluer le système de recommandation.
- **Fonctionnalités réalisées :**
  - Prétraitement et préparation des données de films.
  - Entraînement du modèle de recommandation (Scikit-Learn).
  - Tests de qualité et Data Contracts.
  - Évaluation des performances.
  - Tracking complet et intégration de MLflow pour le suivi des expériences.
  - Gestion des versions du modèle.
- **Contributeurs :** ML Engineers, Data Analysts.
- **Livrables :** Modèle de recommandation entraîné et validé, historique complet des expérimentations dans MLflow.

### Sprint 3 : Déploiement et monitoring (Estimation : 30/06 au 05/07)
L'objectif de ce sprint est de rendre le modèle accessible aux utilisateurs et d'assurer le suivi de son fonctionnement.
- **Fonctionnalités réalisées :**
  - Développement de l'API FastAPI et exposition de `/predict`.
  - Conteneurisation avec Docker.
  - Mise en place du pipeline CI/CD avec GitHub Actions.
  - Monitoring des performances, de la disponibilité, et détection de dérive (drift).
- **Contributeurs :** ML Engineers, Data Engineers.
- **Livrables :** Système de recommandation déployé, API opérationnelle, tableau de bord de monitoring et mécanismes d'alerte.
