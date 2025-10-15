# Sciences Fondamentales

Ce dépôt Git sert à stocker les exercices des mini-boucles du bloc Science Fondamentale de mon école.

## Structure du projet

- `proba.py` : Exercices et scripts liés à la probabilité.
- `stats.py` : Exercices et scripts liés aux statistiques.
- `analyse_server.py` : Script d'analyse des performances serveur et de détection d'anomalies sur les métriques CPU, mémoire, réseau et température.
- `requirements.txt` : Liste des dépendances Python nécessaires pour l'analyse avancée et la génération de graphiques.
- `output/` : Dossier généré automatiquement contenant les graphiques (séries temporelles et histogrammes avec anomalies) pour chaque métrique analysée.
- `dataset/` : Dossier contenant des jeux de données pour les exercices.
    - `server_usage_data.csv` : Données de monitoring serveur (CPU, mémoire, réseau, température).
    - `day.csv` : Données journalières.
    - `hour.csv` : Données horaires.
    - `Readme.txt` : Informations sur les jeux de données.

## Objectif

Ce projet regroupe des exercices pratiques pour renforcer les compétences en sciences fondamentales, notamment en statistiques, probabilités et analyse de données réelles (monitoring serveur, détection d'anomalies, visualisation). Il inclut une étude approfondie des performances système à partir de données de monitoring, avec automatisation de l'analyse et visualisation des résultats.

## Utilisation

1. Clonez le dépôt.
2. Installez les dépendances nécessaires :

```bash
pip install -r requirements.txt
```

3. Pour analyser les performances serveur et détecter les anomalies :

```bash
python analyse_server.py --file dataset/server_usage_data.csv --out output
```

Les graphiques générés seront disponibles dans le dossier `output/`.

Les jeux de données sont disponibles dans le dossier `dataset`.

---

---

*Projet pédagogique pour le bloc Science Fondamentale et l'analyse avancée de données système.*
