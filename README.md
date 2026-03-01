# Nuage ☁️🎮

**Nuage** est une application web de gestion de bibliothèque de jeux vidéo permettant aux utilisateurs d'acheter, de consulter, et de partager des jeux au sein d'une communauté connectée. Ce projet a été développé en binôme (Harris Abassi et Nelson LUU) dans le cadre de la L3 Informatique à l'Université Gustave Eiffel (2024-2025).

---

## 🛠️ Stack Technique

* **Langage :** Python (Script principal `main.py`)
* **Framework Web :** Flask
* **Base de Données :** SQL (Gestion relationnelle via un schéma entité-association mis à jour)
* **Interface :** HTML/CSS (Templates Jinja2 pour le rendu des pages)

---

## 👨‍💻 Répartition des Tâches et Contributions

Le projet a été coordonné via Discord pour assurer une répartition équitable des fonctionnalités et une harmonisation du code.

### 🏗️ Architecture et Logique Serveur (Harris ABASSI)
* **Gestion des Entités Spécifiques :** Développement des pages dédiées par jeux et par profils d'amis.
* **Interactions Dynamiques :** Implémentation des modifications de données via les méthodes HTTP POST pour les formulaires.
* **Harmonisation Technique :** Intégration et fusion des différents modules de code pour assurer la cohérence globale du système.
* **Gestion d'Erreurs :** Debugging croisé et vérification de la robustesse des saisies utilisateurs.

### 🖥️ Interface Utilisateur et Rapports (Nelson LUU)
* **Système de Visualisation :** Création des interfaces de listes, incluant le catalogue global, la bibliothèque personnelle "Mes jeux" et l'annuaire d'amis.
* **Design & Templates :** Conception de l'ensemble des templates graphiques pour assurer une expérience utilisateur fluide.
* **Documentation :** Rédaction du rapport technique final et du guide d'utilisation du projet.
* **Contrôle Qualité :** Revue de code réciproque et tests de navigation sur les pages développées en binôme.

---

## 🚀 Fonctionnalités Principales du Projet

* **Économie Intégrée :** Système "Nuage-Money" permettant aux joueurs de créditer leur compte (ex: 50$) pour effectuer des transactions.
* **Social & Partage :** Possibilité d'ajouter des amis, de consulter leurs succès et de leur partager des jeux possédés (ex: *Adventure Quest*).
* **Catalogue Dynamique :** Tri des jeux par nom, date de parution, ventes, notes moyennes ou genre.
* **Suivi de Progression :** Système de succès (achievements) déblocables par jeu avec affichage du pourcentage de réussite.
* **Feedback Communautaire :** Système de notation (sur 10) et de commentaires modifiables par les utilisateurs.

---

## 🎮 Installation et Utilisation

### Lancement rapide
1. Téléchargez les fichiers dans un dossier de travail.
2. Ouvrez un terminal et exécutez la commande suivante :  
   `python main.py`
3. Cliquez sur le lien local généré (`http://127.0.0.1:5000`) pour accéder à l'interface.

### Guide de navigation
* **Compte :** Inscrivez-vous ou connectez-vous, puis accédez à "Mon compte" pour modifier vos informations ou ajouter des fonds.
* **Achat :** Parcourez la "Liste de nos jeux", sélectionnez un titre (ex: *Fantasy Fighter*) et confirmez l'achat.
* **Avis :** Dans l'onglet "Mes jeux", cliquez sur un titre possédé pour laisser une note ou un commentaire.
* **Amis :** Utilisez l'onglet "Amis" pour rechercher des joueurs, envoyer des demandes et consulter les jeux que vos amis possèdent.
